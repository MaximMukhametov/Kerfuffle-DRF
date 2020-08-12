from .common import *
import dj_database_url

DEBUG = bool(os.environ.get('DJANGO_DEBUG', True))


MIDDLEWARE += (
    'silk.middleware.SilkyMiddleware',
)

INSTALLED_APPS += (
    'silk',
)

