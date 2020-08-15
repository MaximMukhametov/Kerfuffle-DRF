from django.apps import AppConfig


class UsersApiConfig(AppConfig):
    name = 'apps.users'
    verbose_name = 'Users'

    def ready(self):
        import libs.signals
        super().ready()
