from django.db import models

from apps.dialogs.managers import CustomMessageManager


class Message(models.Model):
    """User dialogs."""
    message = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Created time', )
    written_by = models.ForeignKey('users.User', null=True, blank=True,
                                   on_delete=models.CASCADE,
                                   verbose_name='User who wrote this post',
                                   related_name='my_messages',
                                   related_query_name='my_message')
    written_for = models.ForeignKey('users.User', null=True, blank=True,
                                    on_delete=models.CASCADE,
                                    verbose_name='Recipient user of'
                                                 ' this message',
                                    related_name='messages_for_me',
                                    related_query_name='message_for_me')

    objects = CustomMessageManager()

    class Meta:
        ordering = ['created_at']
