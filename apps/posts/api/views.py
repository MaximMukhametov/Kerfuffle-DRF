from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.posts.api.serializers import PostSerializer
from apps.posts.models.post import Post
from apps.posts.permissions import PostChangePermission


class PostView(ModelViewSet):
    """ Provide CRUD workflow with Post model """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, PostChangePermission]

    def perform_create(self, serializer):
        """ Add owner of post """
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        Returns all posts of the user who made the request,
        or posts of the user with the specified number
        """
        user_id = self.request.user.id
        if 'userid' in self.request.query_params:
            user_id = self.request.query_params['userid']
        queryset = Post.objects.filter(owner_id=user_id)
        return queryset


class LikeUnlikeView(APIView):
    """ Provides like / unlike functionality for post instance """
    permission_classes = [IsAuthenticated]

    def put(self, request, **kwargs):
        """
        Puts 'Like' from the current user or
        remove 'Like' if it is already set
        """
        post = get_object_or_404(Post, id=kwargs['pk'])
        is_already_like = request.user.my_likes.filter(id=post.id).exists()
        if is_already_like:
            post.like.remove(request.user)
        else:
            post.like.add(request.user)
        post.save()
        return Response(PostSerializer(post).data)

