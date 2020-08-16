import django_filters
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db.models import QuerySet

__all__ = (
    'UserFilter',
)


class UserFilter(django_filters.FilterSet):
    """Provide filtering user model queryset"""
    followers = django_filters.CharFilter(method='get_qs_by_followers')
    followed = django_filters.CharFilter(method='get_qs_by_followed')
    like_post = django_filters.NumberFilter(method='get_qs_by_like_post')

    class Meta:
        model = get_user_model()
        fields = [
            'name',
            'full_name',
            'status',
            'looking_for_a_job',
            'followers',
            'followed',
            'like_post',
        ]

    @property
    def qs(self) -> QuerySet:
        """By default queryset exclude request user"""
        return super().qs.exclude(id=self.request.user.id)

    def get_qs_by_followers(self, queryset, name, value) -> QuerySet:
        """
        Filtering by followers.
        ----------------------
        If 'true' return all request user followers.
        If 'false' return all users exclude followers by request user.
        """

        if not isinstance(self.request.user, AnonymousUser):
            if value == 'true':
                return queryset.filter(id__in=self.request.user.followers.all())
            elif value == 'false':
                return queryset.exclude(
                    id__in=self.request.user.followers.all())
        return queryset

    def get_qs_by_followed(self, queryset, name, value) -> QuerySet:
        """
        Filtering by following.
        ----------------------
        If 'true' return all users who followed request user.
        If 'false' return all users exclude who followed request user.
        """
        if not isinstance(self.request.user, AnonymousUser):
            if value == 'true':
                return queryset.filter(id__in=self.request.user.followed.all())
            elif value == 'false':
                return queryset.exclude(id__in=self.request.user.followed.all())
        return queryset

    @staticmethod
    def get_qs_by_like_post(queryset, name, value) -> QuerySet:
        """Return all users who liked post by post id"""
        return queryset.filter(my_like__id=value)
