from django.contrib.auth.models import UserManager
from django.db.models import Count
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

    def get_users(self, view, request, post_model):
        """
        Get users with paginate, search by name or by friends.
        """
        error = None
        user = self.model.objects.get(
            id=request.query_params.get('user')) if request.query_params.get(
            'user') else request.user
        users = self.model.objects.exclude(id=request.user.id)
        name = request.query_params.get('name')
        following = request.query_params.get('following')
        followers = request.query_params.get('followers')
        post_id = request.query_params.get('like_post')

        users = self._followers(following, followers, user, users)

        if name:
            users = users.filter(name=name)

        if post_id:
            post = post_model.objects.get(id=post_id)
            users = post.like.all()
        try:
            items = view.paginate_queryset(users, view.request,
                                           view=view)

        except Exception as errors:
            items = None
            error = errors
        return items if items else users, users.count(), error

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
