from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.posts.api.serializers import PostSerializer
from apps.posts.models.post import Post
from apps.posts.permissions import PostChangePermission


class PostView(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, PostChangePermission]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user_id = self.request.user.id
        if 'userid' in self.request.query_params:
            user_id = self.request.query_params['userid']
        queryset = Post.objects.filter(owner_id=user_id)
        return queryset


class LikeUnlikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, **kwargs):
        post = get_object_or_404(Post, id=kwargs['pk'])
        is_already_like = request.user.my_likes.filter(id=post.id).exists()
        if is_already_like:
            post.like.remove(request.user)
        else:
            post.like.add(request.user)
        post.save()
        return Response(PostSerializer(post).data)
