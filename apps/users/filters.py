import django_filters
from django.contrib.auth import get_user_model

__all__ = (
    'UserFilter',
)


class UserFilter(django_filters.FilterSet):
    followers = django_filters.CharFilter(method='get_qs_by_followers')
    following = django_filters.CharFilter(method='get_qs_by_following')
    like_post = django_filters.NumberFilter(method='get_qs_by_like_post')

    class Meta:
        model = get_user_model()
        fields = ['name',
                  'full_name',
                  'status',
                  'looking_for_a_job',
                  'followers',
                  'following',
                  'is_staff',
                  'like_post',
                  'my_like']

    @property
    def qs(self):
        return super().qs.exclude(id=self.request.user.id)

    def get_qs_by_followers(self, queryset, name, value):
        if value == 'true':
            return queryset.filter(id__in=self.request.user.followers.all())
        elif value == 'false':
            return queryset.exclude(id__in=self.request.user.followers.all())
        return queryset

    def get_qs_by_following(self, queryset, name, value):
        if value == 'true':
            return queryset.filter(id__in=self.request.user.followed.all())
        elif value == 'false':
            return queryset.exclude(id__in=self.request.user.followed.all())
        return queryset

    @staticmethod
    def get_qs_by_like_post(queryset, name, value):
        return queryset.filter(my_like__id=value)
