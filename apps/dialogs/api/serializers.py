from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from apps.dialogs.models.message import Message
from apps.users.api.serializers import UserAuthSerializer
from apps.users.models import User


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model."""
    written_by = UserAuthSerializer(required=False)
    written_for = UserAuthSerializer(required=False)
    addressee = serializers.IntegerField(write_only=True)

    class Meta:
        model = Message
        fields = ('id',
                  'message',
                  'created_at',
                  'written_by',
                  'written_for',
                  'addressee',
                  )
        read_only_fields = (
            'created_at',
            'written_by',
            'written_for',
        )

    def create(self, validated_data):
        """
        Create new message and tie it between current user(request.user)
        and user which selected by id(addressee).
        """
        addressee_id = validated_data.pop('addressee')
        addressee = get_object_or_404(User, id=addressee_id)
        message = super().create(validated_data)
        message.written_by = self.context['request'].user
        message.written_for = addressee
        return message


