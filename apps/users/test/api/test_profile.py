import pytest
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from apps.users.models import User

pytestmark = pytest.mark.django_db


def profile_detail_url(user_id: int) -> str:
    """Generate profile url with query params"""
    return reverse('profile-detail', kwargs={'pk': user_id})


def test_get_profile_view(api_auth_client: APIClient,
                          user_factory: type):
    """
    Make sure the profile information for a specific
    user is returned from the profile-detail URL by ID.
    """
    user = user_factory()
    response = api_auth_client.get(profile_detail_url(user.id))

    assert response.status_code == 200
    assert response.data['id'] == user.id


def test_edit_profile_view(faker: Faker,
                           api_auth_client: APIClient,
                           user_with_auth: User):
    """Make sure the user can edit their profile."""
    payload = {'full_name': faker.name(),
               "contacts": {
                   "github": faker.url(),
                   "vk": faker.url(),
                   "facebook": faker.url(),
                   "instagram": faker.url(),
                   "twitter": faker.url(),
                   "website": faker.url(),
                   "youtube": faker.url(),
                   "mainlink": faker.url()
               }
               }
    response = api_auth_client.patch(profile_detail_url(user_with_auth.id),
                                     payload, format='json')
    assert response.status_code == 200
    assert response.data['full_name'] == payload['full_name']

    for payload_contact, response_contact in zip(payload['contacts'].items(),
                                                 response.data[
                                                     'contacts'].items()):
        assert payload_contact == response_contact


def test_edit_profile_not_owned_view(faker: Faker,
                                     api_auth_client: APIClient,
                                     user_factory: type):
    """Make sure that the user can't edit someone else's profile."""
    payload = {'full_name': faker.name()}
    another_user = user_factory()
    response = api_auth_client.patch(profile_detail_url(another_user.id),
                                     payload, format='json')
    assert response.status_code == 403
