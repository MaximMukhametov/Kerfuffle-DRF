import pytest
from django.urls import reverse
from faker import Faker
from rest_framework.test import APIClient

from apps.dialogs.factories import MessageFactory
from apps.dialogs.models import Message
from apps.users.models import User

pytestmark = pytest.mark.django_db


@pytest.fixture(scope='module')
def message_by_auth_user(django_db_setup, django_db_blocker,
                         message_factory: type,
                         user_with_auth: User) -> Message:
    """Return message by auth user."""
    with django_db_blocker.unblock():
        return message_factory(written_by=user_with_auth)


@pytest.fixture(scope='module')
def detail_message_view_url(django_db_blocker,
                            message_by_auth_user: Message) -> str:
    """Return detail view url with message id"""
    return reverse('message-detail', kwargs={'pk': message_by_auth_user.id})


def test_get_message_view(user_factory: type,
                          message_factory: MessageFactory,
                          api_auth_client: APIClient,
                          user_with_auth: User):
    """
    Generate messages between two users, and check last message in response
    """
    messages_amount = 3
    recipient_user = user_factory()
    messages = message_factory.create_batch(written_for=recipient_user,
                                            written_by=user_with_auth,
                                            size=messages_amount)
    last_message = messages[messages_amount - 1]
    response = api_auth_client.get(reverse('message-list'))
    response_message = response.data[0]['message_data']

    assert response.status_code == 200

    assert last_message.id == response_message['id']
    assert last_message.written_by.id == response_message['written_by']['id']
    assert last_message.written_for.id == response_message['written_for']['id']


def test_post_message_view(faker: Faker,
                           user_factory: type,
                           api_auth_client: APIClient,
                           user_with_auth: User):
    """Ensure user can create new message."""
    recipient_user = user_factory()
    payload = {'message': faker.sentence(), 'addressee': recipient_user.id}
    url = reverse('message-list')
    response = api_auth_client.post(url, payload)
    data = response.data

    assert response.status_code == 201

    assert data['message'] == payload['message']
    assert data['written_by']['id'] == user_with_auth.id
    assert data['written_for']['id'] == recipient_user.id


def test_patch_message_view(faker: Faker, message_by_auth_user: Message,
                            api_auth_client: APIClient,
                            detail_message_view_url: str):
    """Ensure user can patch his message."""
    payload = {'message': faker.sentence()}
    response = api_auth_client.patch(detail_message_view_url, payload)

    assert response.status_code == 200

    assert response.data['message'] == payload['message']
    assert response.data['message'] != message_by_auth_user.message


def test_cant_patch_not_owned_message_view(faker: Faker,
                                           user_factory: type,
                                           api_client: APIClient,
                                           detail_message_view_url: str):
    """Ensure user cannot patch not owned message."""
    not_owner = user_factory()
    api_client.force_authenticate(user=not_owner)
    payload = {'message': faker.sentence()}
    response = api_client.patch(detail_message_view_url, payload)

    assert response.status_code == 403


def test_delete_message_view(message_by_auth_user: Message,
                             detail_message_view_url: str,
                             api_auth_client: APIClient):
    """Ensure user can delete his message."""
    response = api_auth_client.delete(detail_message_view_url)

    assert response.status_code == 204

    with pytest.raises(Message.DoesNotExist):
        Message.objects.get(id=message_by_auth_user.id)


def test_cant_delete_not_owned_message_view(message_by_auth_user: Message,
                                            user_factory: type,
                                            api_client: APIClient,
                                            detail_message_view_url):
    """Ensure user cannot delete not owned message."""
    not_owner = user_factory()
    api_client.force_authenticate(user=not_owner)
    response = api_client.delete(detail_message_view_url)

    assert response.status_code == 403

    assert Message.objects.filter(id=message_by_auth_user.id)
