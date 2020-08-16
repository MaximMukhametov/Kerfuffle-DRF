import pytest
from rest_framework.test import APIClient

from apps.dialogs.factories import MessageFactory
from apps.users.factories import UserFactory
from apps.users.models import User


@pytest.fixture(scope="session", autouse=True)
def _setup_django_db(django_db_setup):
    """
    Setup db for all tests.
    It will make sure that the original pytest-django fixture
    is used to create the test database. When other fixtures is
    invoked, the test database is already prepared and configured.
    """


@pytest.fixture(scope='session')
def user_factory(django_db_blocker) -> type:
    with django_db_blocker.unblock():
        return UserFactory


@pytest.fixture(scope='session')
def user_with_auth(django_db_blocker) -> User:
    with django_db_blocker.unblock():
        return UserFactory()


@pytest.fixture(scope='session')
def message_factory(django_db_blocker) -> type:
    return MessageFactory


@pytest.fixture(scope='session')
def api_auth_client(django_db_blocker, user_with_auth) -> APIClient:
    """
    Generate APIClient with authentication
    """
    api_client = APIClient()
    api_client.force_authenticate(user=user_with_auth)
    return api_client


@pytest.fixture(scope='session')
def api_client() -> APIClient:
    return APIClient()
