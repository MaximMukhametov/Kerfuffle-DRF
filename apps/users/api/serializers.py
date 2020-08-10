from collections import OrderedDict

from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers

from apps.contacts.api.serializers import ContactssSerializer
from apps.contacts.models.contact import Contact
from apps.photos.api.serializers import PhotosSerializer
from apps.photos.validators import validate_image
from apps.posts.models.post import Post
from apps.users.models import User


class UserMetaSerializer(serializers.ModelSerializer):
    contacts = ContactssSerializer(required=False)
    photos = PhotosSerializer()
    posts = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('__all__')

    def __init__(self, *args, **kwargs):
        """
        Dynamically include/exclude fields to Django Rest Framwork serializers
        based on properties of this class.
        """

        if 'field_set' in kwargs:
            included = set(kwargs.pop('field_set'))
            super().__init__(*args, **kwargs)
            existing = set(self.fields.keys())
            for other in existing - included:
                self.fields.pop(other)
        else:
            super().__init__(*args, **kwargs)

    @staticmethod
    def get_posts(user):
        from apps.posts.api.serializers import PostSerializer

        """Get all posts of particular user """
        posts = PostSerializer(Post.objects.filter(owner_id=user.id),
                               many=True).data
        return posts

    @staticmethod
    def partial_update(instance, validated_data):
        """Updates user information"""
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

    @staticmethod
    def validate_background_photo(data):
        return validate_image(data)

    def to_representation(self, instance):
        representation = instance
        if isinstance(instance, User):
            representation = super().to_representation(instance)
            representation['followers'] = instance.followers.count()
            representation['following'] = instance.followed.count()
        if 'user' in self.context:
            if not isinstance(self.context[
                                  'user'],
                              AnonymousUser):
                is_followed = self.context['user'].followed.filter(
                    id=instance.id).exists()
                representation['followed'] = True if is_followed else False
        if isinstance(
                instance, OrderedDict) and 'background_photo' in instance and (
                'user_to_get_backgrnd_photo_link' in self.context):
            representation['background_photo'] = self.context[
                'user_to_get_backgrnd_photo_link'].background_photo.url

        return representation
