from rest_framework import serializers

from apps.contacts.models.contact import Contact


class ContactsSerializer(serializers.ModelSerializer):
    """Serializer for Contact model."""

    class Meta:
        model = Contact
        exclude = (
            'github',
            'vk',
            'facebook',
            'instagram',
            'twitter',
            'website',
            'youtube',
            'mainlink')
