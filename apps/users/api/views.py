from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from rest_framework import status
from rest_framework.mixins import UpdateModelMixin, \
    RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet

import apps.users.api.serializer_fields_set as user_fields
from apps.users.api.permissions import CurrentUserIsOwner, \
    CurrentUserIsOwnerAuth
from apps.users.api.serializers import UserMetaSerializer
from apps.users.filters import UserFilter
from apps.users.models import User


class BaseUserViewSet(GenericViewSet):
    """Base generic view set for User model."""
    queryset = User.objects.all()
    serializer_class = UserMetaSerializer
    permission_classes = [IsAuthenticated]


class UsersTotalAPI(ReadOnlyModelViewSet, BaseUserViewSet):
    """
    User view for displaying a list of users and flexible filtering by them.
    """
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserFilter

    def get_serializer(self, *args, **kwargs):
        """Set the required fields for the UserMetaSerializer."""
        return super().get_serializer(field_set=user_fields.user_show_fields,
                                      *args, **kwargs)


class UserProfileView(UpdateModelMixin,
                      RetrieveModelMixin,
                      BaseUserViewSet):
    """
    User view for displaying a profile of particular
    user with detailed information about him.
    """
    permission_classes = (CurrentUserIsOwner,)

    def get_serializer(self, *args, **kwargs):
        """Set the required fields for the UserMetaSerializer."""
        return super().get_serializer(field_set=user_fields.profile_fields,
                                      *args, **kwargs)


class UserAuthView(RetrieveModelMixin, BaseUserViewSet):
    """
    Simple view for auth check.
    """
    permission_classes = (CurrentUserIsOwnerAuth,)

    def get_serializer(self, *args, **kwargs):
        """Set the required fields for the UserMetaSerializer."""
        return super().get_serializer(field_set=user_fields.user_auth_fields,
                                      *args, **kwargs)


class FollowUnfollowView(APIView):
    """Allows you to add or remove a specific user from your followers list."""
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        if request.user.followed.filter(id=kwargs['pk']).exists():
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, **kwargs):
        request.user.follow_unfollow(action='add',
                                     followed_user_id=kwargs['pk'])
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, **kwargs):
        request.user.follow_unfollow(action='remove',
                                     followed_user_id=kwargs['pk'])
        return Response(status=status.HTTP_204_NO_CONTENT)
