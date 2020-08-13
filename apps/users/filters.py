import django_filters
from django.contrib.auth import get_user_model


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(method='my_custom_filter')

    class Meta:
        model = get_user_model()
        fields = ['username',]

    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(**{name: value,})