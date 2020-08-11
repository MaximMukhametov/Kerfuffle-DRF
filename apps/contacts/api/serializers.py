from rest_framework import serializers

from apps.contacts.models.contact import Contact


class ContactsSerializer(serializers.ModelSerializer):
    """Serializer for Contact model."""
    class Meta:
        model = Contact
        exclude = ('id',)