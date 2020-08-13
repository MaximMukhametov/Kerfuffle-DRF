from rest_framework import serializers

from apps.dialogs.models.message import Message
from apps.users.api.serializer_fields_set import user_auth_fields
from apps.users.api.serializers import UserMetaSerializer


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model."""
    written_by = UserMetaSerializer(field_set=user_auth_fields)
    written_for = UserMetaSerializer(field_set=user_auth_fields)

    class Meta:
        model = Message
        fields = ('__all__')



