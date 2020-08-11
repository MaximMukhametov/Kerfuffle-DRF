from rest_framework import serializers

from apps.posts.models.post import Post
from apps.users.api.serializers import UserMetaSerializer
from apps.users.utils import UserFields


class PostSerializer(serializers.ModelSerializer):
    """Serializer for Post model."""

    likes = serializers.CharField(source='likes_count', required=False)
    like = UserMetaSerializer(many=True, read_only=True,
                              field_set=
                              UserFields.user_show_fields)
    user_name = serializers.CharField(source='owner.name', required=False)

    class Meta:
        model = Post
        fields = ('__all__')
