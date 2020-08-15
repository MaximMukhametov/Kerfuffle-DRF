import pytest
from rest_framework.test import APIClient

from apps.dialogs.factories import MessageFactory
from apps.users.factories import UserFactory


@pytest.fixture(scope="session", autouse=True)
def _setup_django_db(django_db_setup):
    """
    Setup db for all tests.
    It will make sure that the original pytest-django fixture
    is used to create the test database. When other fixtures is
    invoked, the test database is already prepared and configured.
    """


@pytest.fixture(scope='session')
def user_factory(django_db_blocker):
    with django_db_blocker.unblock():
        return UserFactory


@pytest.fixture(scope='session')
def user_with_auth(django_db_blocker):
    with django_db_blocker.unblock():
        return UserFactory()


@pytest.fixture(scope='session')
def message_factory(django_db_blocker):
    with django_db_blocker.unblock():
        return MessageFactory


@pytest.fixture(scope='session')
def api_auth_client(django_db_blocker, user_with_auth):
    """
    Generate APIClient with authentication
    """
    api_client = APIClient()
    api_client.force_authenticate(user=user_with_auth)
    return api_client


@pytest.fixture(scope='session')
def api_client():
    return APIClient()
#
#
# @pytest.fixture
# def create_user(db, user_password):
#     def make_user(**kwargs):
#         kwargs['password'] = user_password
#         if 'username' not in kwargs:
#             kwargs['username'] = str(uuid.uuid4())
#         user = get_user_model().objects.create_user(**kwargs)
#         token, _ = Token.objects.get_or_create(user=user)
#         return user
#
#     return make_user