import pytest
from rest_framework.test import APIClient

from apps.users.models import User

pytestmark = pytest.mark.django_db


def test_get_users_view(user_factory: type,
                        api_auth_client: APIClient,
                        user_with_auth: User):
    """Ensure user can see all users."""
