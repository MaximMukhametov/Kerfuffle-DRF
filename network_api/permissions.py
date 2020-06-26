from rest_framework import permissions


class PostChangePermission(permissions.BasePermission):
    message = 'You have not permission to modify this post.'

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
