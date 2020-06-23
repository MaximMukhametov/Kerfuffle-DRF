from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .managers import CustomUserManager, CustomMessageManager


class Message(models.Model):
    message = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Created time', )
    written_by = models.ForeignKey('User', null=True, blank=True,
                                   on_delete=models.CASCADE,
                                   verbose_name='Written by',
                                   related_name='my_messages',
                                   related_query_name='my_message')
    written_for = models.ForeignKey('User', null=True, blank=True,
                                    on_delete=models.CASCADE,
                                    verbose_name='Written for',
                                    related_name='messages_for_me',
                                    related_query_name='message_for_me')

    objects = CustomMessageManager()

    class Meta:
        ordering = ['created_at']


class Contact(models.Model):
    github = models.CharField(null=True, blank=True, max_length=100)
    vk = models.CharField(null=True, blank=True, max_length=100)
    facebook = models.CharField(null=True, blank=True, max_length=100)
    instagram = models.CharField(null=True, blank=True, max_length=100)
    twitter = models.CharField(null=True, blank=True, max_length=100)
    website = models.CharField(null=True, blank=True, max_length=100)
    youtube = models.CharField(null=True, blank=True, max_length=100)
    mainlink = models.CharField(null=True, blank=True, max_length=100)


class Photo(models.Model):
    small = models.TextField(null=True, blank=True, verbose_name='Small')
    small_img = models.ImageField(null=True, blank=True,
                                  verbose_name='Small img')
    large = models.TextField(null=True, blank=True, verbose_name='Large')
    large_img = models.ImageField(null=True, blank=True,
                                  verbose_name='Large img')


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50, unique=True, verbose_name='Name')
    unique_url_name = models.CharField(null=True, blank=True, max_length=50,
                                       verbose_name='Url name')
    full_name = models.CharField(null=True, blank=True, max_length=50,
                                 verbose_name='Full name')
    photos = models.OneToOneField(Photo, null=True, blank=True,
                                  on_delete=models.SET_NULL)
    background_photo = models.ImageField(null=True, blank=True,
                                         verbose_name='background_photo')
    status = models.CharField(null=True, blank=True, max_length=50,
                              verbose_name='Status')
    followed = models.ManyToManyField('self', blank=True, symmetrical=False,
                                      related_name='followers')
    is_staff = models.BooleanField(default=False)
    contacts = models.OneToOneField(Contact, null=True, blank=True,
                                    on_delete=models.SET_NULL)
    looking_for_a_job = models.BooleanField(null=True, blank=True,
                                            verbose_name='Looking for a job')
    looking_for_a_job_description = models.TextField(null=True, blank=True,
                                                     verbose_name=
                                                     'Looking for a job description')

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        ordering = ['-id']

    @staticmethod
    @receiver(post_save, sender='network_api.User')
    def create_contacts_for_new_user(sender, created, instance, **kwargs):
        if created:
            instance.contacts = Contact.objects.create()
            instance.save()


class Post(models.Model):
    text = models.TextField()
    owner = models.ForeignKey(User, null=True, blank=True,
                              on_delete=models.CASCADE,
                              related_name='my_posts')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Created time')
    like = models.ManyToManyField(User, verbose_name='Like',
                                  related_name='my_likes',
                                  related_query_name='my_like')

    class Meta:
        ordering = ['-created_at']

    @property
    def likes_count(self):
        likes = self.like.count()
        return likes
