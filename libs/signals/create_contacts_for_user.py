from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.contacts.models.contact import Contact


@receiver(post_save, sender='users.User')
def create_contacts_for_new_user(sender, created, instance, **kwargs):
    """Creating a contact entity when creating a user"""
    if created:
        instance.contacts = Contact.objects.create()
        instance.save()
