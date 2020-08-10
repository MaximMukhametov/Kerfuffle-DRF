from rest_framework import serializers

from apps.contacts.models.contact import Contact


class ContactssSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        exclude = ('id',)