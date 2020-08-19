import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from apps.users.models import User

pytestmark = pytest.mark.django_db


def user_list_url_with_filter(filter_pattern: str) -> str:
    """Generate url with query params"""
    return ''.join([reverse('users-list'), f'?{filter_pattern}'])


def test_get_users_view(api_client: APIClient):
    """Ensure anybody can see all users."""
    url = reverse('users-list')
    response = api_client.get(url)

    assert response.status_code == 200


@pytest.mark.parametrize(
    'bool_value, user_count_change', [('true', 1), ('false', -1)]
)
@pytest.mark.parametrize(
    'filter_pattern', ['followers', 'followed', ]
)
@pytest.mark.django_db
def test_users_view_with_follow_filter(bool_value: str,
                                       user_count_change: int,
                                       filter_pattern: str,
                                       api_auth_client: APIClient,
                                       user_with_auth: User,
                                       user_factory: type):
    """
    Ensure user view filter by followers/followed works.

    This test has a double parameterization
    that generates 4 tests:
                            .../?followers=true
                            .../?followers=false
                            .../?followed=true
                            .../?followed=false
    """
    some_user = user_factory()
    crowd_amount = 3
    user_factory.create_batch(size=crowd_amount)
    url = user_list_url_with_filter(''.join((filter_pattern, '=', bool_value)))
    response = api_auth_client.get(url)

    if bool_value == 'true':
        test_count_of_users = getattr(user_with_auth, filter_pattern).count()
    else:
        test_count_of_users = User.objects.all().exclude(
            id=user_with_auth.id).count()

    assert response.status_code == 200
    assert response.data['count'] == test_count_of_users

    getattr(user_with_auth, filter_pattern).add(some_user)
    response = api_auth_client.get(url)

    assert response.status_code == 200
    assert response.data['count'] == test_count_of_users + user_count_change

