from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.dialogs.api.serializers import MessageSerializer
from apps.dialogs.models.message import Message
from apps.users.models import User


class MessageView(APIView):
    """Provide CRUD api for Message model."""
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        """Retrieve all message, or all message between particular user."""
        if 'get_users' in request.query_params:
            correspondence = Message.objects.get_users(request,
                                                       self.serializer_class)
            return Response(correspondence)

        message, count = Message.objects.get_messages(request, kwargs['pk'])
        serializer = self.serializer_class(message, many=True)
        return Response({'count': count, 'data': serializer.data})

    def post(self, request, **kwargs):
        """Create new message between two users."""
        addressee = get_object_or_404(User, id=kwargs['pk'])
        new_message = Message.objects.create(addressee, request)
        serializer = self.serializer_class(new_message)
        new_message.save()
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        """Edit message by 'pk'."""
        mutable_message = get_object_or_404(request.user.my_messages,
                                            id=kwargs['pk'])
        mutable_message.message = request.data['message']
        serializer = self.serializer_class(mutable_message)
        mutable_message.save(update_fields=['message'])
        return Response(serializer.data)

    def delete(self, request, **kwargs):
        """Delete message by 'pk'."""
        message_to_be_deleted = get_object_or_404(request.user.my_messages,
                                                  id=kwargs['pk'])
        result, _ = message_to_be_deleted.delete()
        return Response(
            status=status.HTTP_200_OK if result else status.HTTP_400_BAD_REQUEST)
