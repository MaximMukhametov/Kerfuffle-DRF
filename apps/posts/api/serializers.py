from rest_framework import serializers

from apps.posts.models.post import Post
from apps.users.api.serializers import UserMetaSerializer


class PostSerializer(serializers.ModelSerializer):
    """Serializer for Post model."""

    likes = serializers.CharField(source='likes_count', required=False)
    like = UserMetaSerializer(many=True, read_only=True)
    user_name = serializers.CharField(source='owner.name', required=False)

    class Meta:
        model = Post
        fields = (
            'id',
            'text',
            'owner',
            'user_name',
            'created_at',
            'like',
            'likes')
