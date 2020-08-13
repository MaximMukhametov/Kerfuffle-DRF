from rest_framework import serializers

from apps.dialogs.models.message import Message
from apps.users.api.serializers import UserAuthSerializer


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model."""
    written_by = UserAuthSerializer()
    written_for = UserAuthSerializer()

    class Meta:
        model = Message
        fields = ('message', 'created_at', 'written_by', 'written_for')
