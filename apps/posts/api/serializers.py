from rest_framework import serializers

from apps.posts.models.post import Post
from apps.users.utils import UserFields


class PostSerializer(serializers.ModelSerializer):
    from apps.users.api.serializers import UserMetaSerializer

    likes = serializers.CharField(source='likes_count', required=False)
    like = UserMetaSerializer(many=True, read_only=True,
                              field_set=UserFields.user_show_fields)

    class Meta:
        model = Post
        fields = ('__all__')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user_name'] = instance.owner.name
        representation['created_at'] = instance.created_at.strftime(
            "%m/%d/%Y %H:%M:%S")
        return representation
