from django.db import models
from django.db.models import Q
from rest_framework.exceptions import ValidationError


class CustomMessageManager(models.Manager):
    def get_users(self, request, serializer_class):
        """
        Gives a list of users who have correspondence
        with a particular user with the last message
        """
        filter = Q(message_for_me__written_by_id=request.user.id) | Q(
            my_message__written_for_id=request.user.id)
        chat_users = request.user.__class__.objects.filter(filter).values_list(
            'id',
            'name').distinct()
        messages_with_chat_users = []
        for key, name in chat_users:
            messages, _ = self.get_messages(request, key, count=1, order='-')
            last_message = serializer_class(messages[0])
            messages_with_chat_users.append({'id': key, 'name': name,
                                             'messagedata': last_message.data})
        return messages_with_chat_users

    def get_messages(self, request, target_user_id, count=10,
                     order='-'):
        """
        Gives a list of dialogs between current user
        and user which selected by id, with the ability to
        limit the quantity of dialogs by 'count'
        """
        if 'count' in request.query_params:
            count = int(request.query_params['count'])
        if count < 0:
            raise ValidationError(
                f'The "count" cannot be negative, you put {count}')
        filter = Q(written_for_id=request.user.id,
                   written_by_id=target_user_id) | Q(
            written_by_id=request.user.id, written_for_id=target_user_id)
        messages = self.filter(filter).order_by(f'{order}created_at')
        counter = messages.count()
        return messages[:count], counter

    def create(self, addressee, request):
        """
        Create new message and tie it between current user(request.user)
        and user which selected by id(addressee)
        """
        new_message = self.model(written_for=addressee,
                                 written_by=request.user,
                                 message=request.data['message'])
        return new_message
