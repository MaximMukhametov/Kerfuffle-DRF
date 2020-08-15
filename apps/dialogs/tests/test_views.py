import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def get_message_view_url():
    return reverse('message_list')


def test_get_message_view(user_factory, message_factory, user_api_auth_client):
    """
    Generate messages between two users, and check last message in response
    """
    messages_amount = 3
    user_message_owner, api_client = user_api_auth_client
    recipient_user = user_factory()
    messages = message_factory.create_batch(written_for=recipient_user,
                                            written_by=user_message_owner,
                                            size=messages_amount)
    last_message = messages[messages_amount - 1]
    url = get_message_view_url()
    response = api_client.get(url)
    response_message = response.data[0]['message_data']
    assert last_message.id == response_message['id']
    assert last_message.written_by.id == response_message['written_by']['id']
    assert last_message.written_for.id == response_message['written_for']['id']



def test_post_message_view(faker,
                         user_factory,
                         message_factory,
                         user_api_auth_client):
    pass

def test_patch_message_view(faker,
                         user_factory,
                         message_factory,
                         user_api_auth_client):
    pass


def test_delete_message_view(faker,
                         user_factory,
                         message_factory,
                         user_api_auth_client):
    pass