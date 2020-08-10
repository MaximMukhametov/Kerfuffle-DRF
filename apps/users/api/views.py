from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.posts.models.post import Post
from apps.users.api.serializers import UserMetaSerializer
from apps.users.models import User
from apps.users.utils import UserFields


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


class UserAuthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserMetaSerializer(request.user,
                                        field_set=UserFields.user_auth_fields)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
