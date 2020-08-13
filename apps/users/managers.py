from django.contrib.auth.models import UserManager
from rest_framework import status
from rest_framework.response import Response


class CustomUserManager(UserManager):
    def _create_user(self, name, password, **extra_fields):
        """
        Create and save a user with the given name, and password.
        """
        if not name:
            raise ValueError('The given name must be set')
        name = self.model.normalize_username(name)
        user = self.model(name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, name, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(name, password, **extra_fields)

    def create_superuser(self, name, password, **extra_fields):
        """
        Create and save a SuperUser with the given name and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(name, password, **extra_fields)

    def follow_unfollow(self, user, action, followed_user_id):
        """
        Accepts action(add or remove) and edit list of user friends.
        """
        try:
            followed_user = self.model.objects.get(id=followed_user_id)
            getattr(user.followed, action)(followed_user)
            return Response(status=status.HTTP_200_OK)
        except self.model.DoesNotExist:
            return Response(f'User number {followed_user_id} not found ',
                            status=status.HTTP_404_NOT_FOUND)

    def _followers(self, following, followers, user, users):
        if following:
            if following == 'true':
                users = user.followed.all()
            elif following == 'false':
                users = self.model.objects.exclude(
                    id__in=user.followed.all())

        if followers:
            if followers == 'true':
                users = user.followers.all()
            elif followers == 'false':
                users = self.model.objects.exclude(
                    id__in=user.followers.all())
        return users
