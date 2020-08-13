from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

import apps.users.api.serializer_fields_set as user_fields
from apps.users.api.serializers import UserMetaSerializer
from apps.users.filters import UserFilter
from apps.users.models import User

user_response = openapi.Response('UserApi response', UserMetaSerializer)


class UsersTotalAPI(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserMetaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserFilter

    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(field_set=user_fields.user_show_fields,
                                      *args, **kwargs)


class UserProfileView(APIView):

    def get(self, request, **kwargs):
        user = User.objects.get(id=kwargs['pk'] if kwargs else request.user.id)
        serializer = UserMetaSerializer(user,
                                        field_set=user_fields.profile_contacts_get_fields)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @permission_classes(IsAuthenticated)
    def patch(self, request):
        serializer = UserMetaSerializer(data=request.data, partial=True,
                                        context={
                                            'user_to_get_background_photo_link': request.user},
                                        field_set=user_fields.profile_contacts_put_fields)
        serializer.is_valid(raise_exception=True)
        serializer.partial_update(request.user, serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserStatusView(APIView):
    serializer_class = UserMetaSerializer

    def get(self, request, **kwargs):
        user = User.objects.get(id=kwargs['pk'] if kwargs else request.user.id)
        serializer = self.serializer_class(user,
                                           field_set=user_fields.status_fields)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @permission_classes(IsAuthenticated)
    def put(self, request):
        serializer = self.serializer_class(data=request.data,
                                           field_set=user_fields.status_fields)
        if serializer.is_valid():
            request.user.status = serializer.data['status']
            request.user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAuthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserMetaSerializer(request.user,
                                        field_set=user_fields.user_auth_fields)
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
