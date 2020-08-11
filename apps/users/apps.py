from django.apps import AppConfig


class UsersApiConfig(AppConfig):
    name = 'apps.users'
    verbose_name = 'Users'

    def ready(self):
        super().ready()
