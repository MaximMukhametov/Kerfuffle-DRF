import factory


class UserFactory(factory.django.DjangoModelFactory):
    """
    Factory for generates test User model.
    There are required field 'name'.
    """
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
