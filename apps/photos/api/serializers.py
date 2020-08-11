from rest_framework import serializers

from apps.photos.models.photo import Photo
from apps.photos.utils import get_resize_image
from apps.photos.validators import validate_image


class PhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('__all__')


class PhotosUploadSerializer(serializers.ModelSerializer):
    """Serializer for Photo model."""
    class Meta:
        model = Photo
        fields = ('large_img',)

    @staticmethod
    def validate_large_img(data):
        """Checks if the image size is exceeded"""
        return validate_image(data)

    def create(self, validated_data):
        """
        Update or create photo instance, and associates with particular user
        """
        user = validated_data['user']
        validated_data['large_img'].name = f'{user.id}{user.name}.jpg'
        photo_obj, is_create = Photo.objects.update_or_create(
            id=user.photos_id, defaults=validated_data)

        get_resize_image(photo_obj.large_img, photo_obj.small_img)

        if is_create:
            user.photos = photo_obj
        user.save()
        return photo_obj
