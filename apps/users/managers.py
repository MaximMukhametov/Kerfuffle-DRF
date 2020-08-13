from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    def _create_user(self, name, password, **extra_fields):
        """
        Create and save a user with the given name, and password.
        """
        if not name:
            raise ValueError('The given name must be set')
        name = self.model.normalize_username(name)
        user = self.model(name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, name, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(name, password, **extra_fields)

    def create_superuser(self, name, password, **extra_fields):
        """
        Create and save a SuperUser with the given name and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(name, password, **extra_fields)
