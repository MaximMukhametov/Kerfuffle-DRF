from collections import OrderedDict

from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers

from network_api.models import User, Photo, Contact, Message, Post
from network_api.utils import get_resize_image, UserFields
from network_api.validators.image_upload_validator import validate_image


class PhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('__all__')


class PhotosUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('large_img',)

    def validate_large_img(self, data):
        return validate_image(self, data)

    def create(self, validated_data):
        user = validated_data['user']
        validated_data['large_img'].name = f'{user.id}{user.name}.jpg'
        photo_obj, is_create = Photo.objects.update_or_create(
            id=user.photos_id, defaults=validated_data)

        get_resize_image(photo_obj.large_img, photo_obj.small_img)

        if is_create:
            user.photos = photo_obj
        user.save()
        return photo_obj


class ContactssSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        exclude = ('id',)


class UserMetaSerializer(serializers.ModelSerializer):
    contacts = ContactssSerializer(required=False)
    photos = PhotosSerializer()
    posts = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('__all__')

    def __init__(self, *args, **kwargs):
        if 'field_set' in kwargs:
            included = set(kwargs.pop('field_set'))
            super().__init__(*args, **kwargs)
            existing = set(self.fields.keys())
            for other in existing - included:
                self.fields.pop(other)
        else:
            super().__init__(*args, **kwargs)

    def get_posts(self, user):
        posts = PostSerializer(Post.objects.filter(owner_id=user.id),
                               many=True).data
        return posts

    def partial_update(self, instance, validated_data):
        is_contacts = False
        if 'contacts' in validated_data.keys():
            is_contacts = True
            contacts_validated_data = validated_data.pop('contacts')
            isvalid = ContactssSerializer(data=contacts_validated_data)
            isvalid.is_valid(raise_exception=True)
            instance.contacts = \
                Contact.objects.update_or_create(id=instance.contacts_id,
                                                 defaults=
                                                 contacts_validated_data)[0]
        [setattr(instance, attr, value) for attr, value in
         validated_data.items()]
        instance.save()
        if is_contacts:
            validated_data['contacts'] = contacts_validated_data
        return instance

    def validate_background_photo(self, data):
        return validate_image(self, data)

    def to_representation(self, instance):
        representation = instance
        if isinstance(instance, User):
            representation = super().to_representation(instance)
            representation['followers'] = instance.followers.count()
            representation['following'] = instance.followed.count()
        if 'user' in self.context:
            if not isinstance(self.context[
                                  'user'],
                              AnonymousUser):  # пересмотреть, мб убрать
                is_followed = self.context['user'].followed.filter(
                    id=instance.id).exists()
                representation['followed'] = True if is_followed else False
        if isinstance(
                instance, OrderedDict) and 'background_photo' in instance and (
                'user_to_get_backgrnd_photo_link' in self.context):
            representation['background_photo'] = self.context[
                'user_to_get_backgrnd_photo_link'].background_photo.url

        return representation


class MessageSerializer(serializers.ModelSerializer):
    user_sourse = UserMetaSerializer

    class Meta:
        model = Message
        fields = ('__all__')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['written_by'] = self.user_sourse(
            instance.written_by, field_set=UserFields.user_auth_fields).data
        representation['written_for'] = self.user_sourse(
            instance.written_for, field_set=UserFields.user_auth_fields).data
        representation['created_at'] = instance.created_at.strftime(
            "%m/%d/%Y %H:%M:%S")
        return representation


class PostSerializer(serializers.ModelSerializer):
    likes = serializers.CharField(source='likes_count', required=False)
    like = UserMetaSerializer(many=True, read_only=True,
                              field_set=UserFields.user_show_fields)

    class Meta:
        model = Post
        fields = ('__all__')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user_name'] = instance.owner.name
        representation['created_at'] = instance.created_at.strftime(
            "%m/%d/%Y %H:%M:%S")
        return representation
