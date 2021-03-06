# Generated by Django 3.0.7 on 2020-08-11 08:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dialogs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='written_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='my_messages', related_query_name='my_message', to=settings.AUTH_USER_MODEL, verbose_name='User who wrote this post'),
        ),
        migrations.AddField(
            model_name='message',
            name='written_for',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages_for_me', related_query_name='message_for_me', to=settings.AUTH_USER_MODEL, verbose_name='Recipient user of this message'),
        ),
    ]
