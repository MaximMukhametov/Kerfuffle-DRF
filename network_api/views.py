from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from network_api.models import User, Photo, Message, Post
from network_api.permissions import PostChangePermission
from network_api.serializers import PhotosUploadSerializer, \
    PhotosSerializer, MessageSerializer, PostSerializer, UserMetaSerializer
from network_api.utils import UserFields


class UsersTotalAPI(APIView, PageNumberPagination):
    permission_classes = [IsAuthenticated]
    page_query_param = 'page'
    page_size_query_param = 'count'
    max_page_size = 100

    def get(self, request):
        users, users_count, error = User.objects.get_users(self, request,
                                                           post_model=Post)

        user_serializer = UserMetaSerializer(users,
                                             context={'user': request.user},
                                             many=True,
                                             field_set=UserFields.user_show_fields)

        return Response({"items": user_serializer.data,
                         "totalCount": users_count, "error": error})


class UserProfileView(APIView):

    def get(self, request, **kwargs):
        user = User.objects.get(id=kwargs['pk'] if kwargs else request.user.id)
        serializer = UserMetaSerializer(user,
                                        field_set=UserFields.profile_contacts_get_fields)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @permission_classes(IsAuthenticated)
    def patch(self, request):
        serializer = UserMetaSerializer(data=request.data, partial=True,
                                        context={
                                            'user_to_get_backgrnd_photo_link': request.user},
                                        field_set=UserFields.profile_contacts_put_fields)
        serializer.is_valid(raise_exception=True)
        serializer.partial_update(request.user, serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserStatusView(APIView):
    serializer_class = UserMetaSerializer

    def get(self, request, **kwargs):
        user = User.objects.get(id=kwargs['pk'] if kwargs else request.user.id)
        serializer = self.serializer_class(user,
                                           field_set=UserFields.status_fields)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @permission_classes(IsAuthenticated)
    def put(self, request):
        serializer = self.serializer_class(data=request.data,
                                           field_set=UserFields.status_fields)
        if serializer.is_valid():
            request.user.status = serializer.data['status']
            request.user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PhotoUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        photo = Photo.objects.get(user=request.user.id)
        serializer = PhotosSerializer(photo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):

        photo_serializer = PhotosUploadSerializer(data=request.data)

        if photo_serializer.is_valid():
            photo_serializer.save(user=request.user)
            response_serializer = PhotosSerializer(photo_serializer.instance)
            return Response(response_serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(photo_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class UserAuthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserMetaSerializer(request.user,
                                        field_set=UserFields.user_auth_fields)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MessageView(APIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        if 'get_users' in request.query_params:
            correspondence = Message.objects.get_users(request,
                                                       self.serializer_class)
            return Response(correspondence)

        message, count = Message.objects.get_messages(request, kwargs['pk'])
        serializer = self.serializer_class(message, many=True)
        return Response({'count': count, 'data': serializer.data})

    def post(self, request, **kwargs):
        addressee = get_object_or_404(User, id=kwargs['pk'])
        new_message = Message.objects.create(addressee, request)
        serializer = self.serializer_class(new_message)
        new_message.save()
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        mutable_message = get_object_or_404(request.user.my_messages,
                                            id=kwargs['pk'])
        mutable_message.message = request.data['message']
        serializer = self.serializer_class(mutable_message)
        mutable_message.save(update_fields=['message'])
        return Response(serializer.data)

    def delete(self, request, **kwargs):
        message_to_be_deleted = get_object_or_404(request.user.my_messages,
                                                  id=kwargs['pk'])
        result, _ = message_to_be_deleted.delete()
        return Response(
            status=status.HTTP_200_OK if result else status.HTTP_400_BAD_REQUEST)


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


class FollowUnfollowView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        if request.user.followed.filter(id=kwargs['pk']).exists():
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, **kwargs):
        return User.objects.follow_unfollow(user=request.user, action='add',
                                            followed_user_id=kwargs['pk'])

    def delete(self, request, **kwargs):
        return User.objects.follow_unfollow(user=request.user, action='remove',
                                            followed_user_id=kwargs['pk'])


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
