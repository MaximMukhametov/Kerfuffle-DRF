import factory

from apps.users.factories import UserFactory


class MessageFactory(factory.django.DjangoModelFactory):
    """Factory for generates test Message model."""

    written_for = factory.SubFactory(UserFactory)
    written_by = factory.SubFactory(UserFactory)
    message = factory.Faker('sentence')

    class Meta:
        model = 'dialogs.Message'
