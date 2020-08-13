from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers

import apps.posts.api as post_api
from apps.contacts.api.serializers import ContactsSerializer
from apps.contacts.models.contact import Contact
from apps.photos.api.serializers import PhotosSerializer
from apps.photos.validators import validate_image
from apps.posts.models.post import Post
from apps.users.models import User


class UserMetaSerializer(serializers.ModelSerializer):
    """
    Instead of creating many serializers, a single meta serializer
    was created, with dynamically changing fields.
     """

    contacts = ContactsSerializer(required=False, many=True)
    photos = PhotosSerializer(many=True)
    posts = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    followed = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'name', 'unique_url_name',
                  'full_name', 'posts', 'photos', 'background_photo',
                  'status', 'followed', 'followers', 'looking_for_a_job',
                  'looking_for_a_job_description', 'contacts', 'following')

    def __init__(self, *args, **kwargs):
        """
        Dynamically include/exclude fields to Django Rest Framework
        serializers based on properties of this class.
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
    def partial_update(instance, validated_data):
        """Updates user information."""
        is_contacts = False
        if 'contacts' in validated_data.keys():
            is_contacts = True
            contacts_validated_data = validated_data.pop('contacts')
            isvalid = ContactsSerializer(data=contacts_validated_data)
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
    def get_posts(user):
        """Get all posts of particular user."""
        return post_api.serializers.PostSerializer(
            Post.objects.filter(owner_id=user.id), many=True).data

    @staticmethod
    def validate_background_photo(data):
        """Validate image size."""
        return validate_image(data)

    @staticmethod
    def get_followers(obj):
        """Return amount of followers."""
        return obj.followers.count()

    @staticmethod
    def get_followed(obj):
        """Return amount of followed users of request user."""
        return obj.followed.count()

    def get_following(self, obj):
        """Checks if the request user is following the particular user."""
        is_followed = False
        user = self.context['request'].user
        if not isinstance(user, AnonymousUser):
            is_followed = user.followed.filter(
                id=obj.id).exists()
        return bool(is_followed)
