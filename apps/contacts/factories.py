import factory


class ContactFactory(factory.django.DjangoModelFactory):
    """
    Factory for generates test Contact model.
    """

    class Meta:
        model = 'contacts.Contact'

    github = factory.Faker('url')
    vk = factory.Faker('url')
    facebook = factory.Faker('url')
    instagram = factory.Faker('url')
    twitter = factory.Faker('url')
    website = factory.Faker('url')
    youtube = factory.Faker('url')
    mainlink = factory.Faker('url')
