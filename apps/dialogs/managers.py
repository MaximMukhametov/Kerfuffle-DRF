from django.db import models
from django.db.models import Q, QuerySet

from apps.users.models import User


class CustomMessageManager(models.Manager):
    def get_users(self, user: User, serializer_class: type) -> list:
        """
        Gives a list of users who have correspondence
        with a particular user with the last message.
        """
        filter = Q(message_for_me__written_by_id=user.id) | Q(
            my_message__written_for_id=user.id)
        chat_users = user.__class__.objects.filter(filter).values_list(
            'id', 'name').distinct()
        messages_with_chat_users = []
        for key, name in chat_users:
            messages = self.get_messages(user, key)
            last_message = serializer_class(messages[0])
            messages_with_chat_users.append({'id': key, 'name': name,
                                             'message_data': last_message.data})
        return messages_with_chat_users

    def get_messages(self, user: User, target_user_id: int) -> QuerySet:
        """
        Gives a list of dialogs between current user
        and user which selected by id, with the ability to
        limit the quantity of dialogs by 'count'.
        """
        filter = Q(written_for_id=user.id,
                   written_by_id=target_user_id) | Q(
            written_by_id=user.id, written_for_id=target_user_id)
        return self.filter(filter).order_by('-created_at')
