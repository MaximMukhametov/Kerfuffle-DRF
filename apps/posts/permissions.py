from rest_framework import permissions


class PostChangePermission(permissions.BasePermission):
    """
    Check if request.user is the same user that is
    contained within the obj then allows
    """
    message = 'You have not permission to modify this post.'

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
