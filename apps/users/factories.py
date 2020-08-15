import factory

from apps.contacts.factories import ContactFactory


class UserFactory(factory.django.DjangoModelFactory):
    """
    Factory for generates test User model.
    There are required field 'name'.
    """
    contacts = factory.RelatedFactory(ContactFactory,
                                      factory_related_name='user')
    name = factory.Faker('name')
    full_name = factory.Faker('name')
    status = factory.Faker('sentence')

    class Meta:
        model = 'users.User'
        django_get_or_create = ('name',)

    @factory.post_generation
    def followed(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # add extracted user to followed
            self.followed.add(extracted)


    @factory.post_generation
    def create_messages(self, create, extracted, **kwargs):
        pass
#
# class UserWithAvatarFactory(UserFactory):
#     """Custom factory for testing user with avatar.
#
#     The factory creates really user avatar file.
#
#     """
#     avatar = factory.django.ImageField(color='magenta')
