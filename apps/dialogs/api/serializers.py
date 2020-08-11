from rest_framework import serializers

from apps.dialogs.models.message import Message
from apps.users.api.serializers import UserMetaSerializer
from apps.users.utils import UserFields


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model."""
    user_sourse = UserMetaSerializer

    class Meta:
        model = Message
        fields = ('__all__')

    def to_representation(self, instance):
        """Add extra information about messages"""
        representation = super().to_representation(instance)
        representation['written_by'] = self.user_sourse(
            instance.written_by, field_set=UserFields.user_auth_fields).data
        representation['written_for'] = self.user_sourse(
            instance.written_for, field_set=UserFields.user_auth_fields).data
        return representation
