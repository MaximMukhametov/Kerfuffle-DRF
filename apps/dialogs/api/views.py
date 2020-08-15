from rest_framework.decorators import action
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.dialogs.api.serializers import MessageSerializer
from apps.dialogs.models.message import Message


class MessageModelViewSet(ModelViewSet):
    """Provide CRUD api for Message model."""
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    queryset = Message.objects.all()

    @action(detail=True)
    def message(self, request, **kwargs):
        """Retrieve all message between particular user"""
        message = Message.objects.get_messages(request.user, kwargs['pk'])
        page = self.paginate_queryset(message)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(message, many=True)
        return Response(serializer.data)

    def list(self, request, **kwargs):
        """
        Gives a list of users who have correspondence
        with a particular user with the last message.
        """
        correspondence = Message.objects.get_users(request.user,
                                                   self.serializer_class)
        return Response(correspondence)
