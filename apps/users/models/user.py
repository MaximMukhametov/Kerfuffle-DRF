from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from rest_framework.exceptions import ValidationError

from apps.users.managers import CustomUserManager


__all__ = (
    'User',
)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=60, unique=True, verbose_name='Name')
    unique_url_name = models.CharField(null=True, blank=True, max_length=60,
                                       verbose_name='Url name')
    full_name = models.CharField(null=True, blank=True, max_length=60,
                                 verbose_name='Full name')
    photos = models.OneToOneField('photos.Photo', null=True, blank=True,
                                  on_delete=models.SET_NULL)
    background_photo = models.ImageField(null=True, blank=True,
                                         verbose_name='Background photo')
    status = models.CharField(null=True, blank=True, max_length=60,
                              verbose_name='Status')
    followed = models.ManyToManyField('self', blank=True, symmetrical=False,
                                      verbose_name='Users to follow',
                                      related_name='followers')
    is_staff = models.BooleanField(default=False)
    contacts = models.OneToOneField('contacts.Contact', null=True, blank=True,
                                    verbose_name='Social network links',
                                    on_delete=models.SET_NULL)
    looking_for_a_job = models.BooleanField(null=True, blank=True,
                                            verbose_name='Looking for a job')
    looking_for_a_job_description = models.TextField(null=True, blank=True,
                                                     verbose_name=
                                                     'Looking for a job description')

    USERNAME_FIELD = 'name'
    objects = CustomUserManager()

    class Meta:
        ordering = ['-id']

    def follow_unfollow(self, action, followed_user_id):
        """
        Accepts action(add or remove) and edit list of user friends.
        """

        if self.followed.filter(id=followed_user_id).exists():
            followed_user = self.__class__.objects.get(id=followed_user_id)
            getattr(self.followed, action)(followed_user)
            return
        raise ValidationError(f'User number {followed_user_id} not found ')
