from rest_framework import serializers

from apps.dialogs.models.message import Message
from apps.users.api.serializers import UserMetaSerializer
from apps.users.utils import UserFields


class MessageSerializer(serializers.ModelSerializer):
    user_sourse = UserMetaSerializer

    class Meta:
        model = Message
        fields = ('__all__')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['written_by'] = self.user_sourse(
            instance.written_by, field_set=UserFields.user_auth_fields).data
        representation['written_for'] = self.user_sourse(
            instance.written_for, field_set=UserFields.user_auth_fields).data
        representation['created_at'] = instance.created_at.strftime(
            "%m/%d/%Y %H:%M:%S")
        return representation
