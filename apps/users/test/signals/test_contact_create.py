import pytest

pytestmark = pytest.mark.django_db


def test_contacts_create(user_factory: type):
    """
    Make sure that when the User instance was created,
    Contact instance was created automatically
    """
    user = user_factory()
    contact = user.contacts
    assert contact
