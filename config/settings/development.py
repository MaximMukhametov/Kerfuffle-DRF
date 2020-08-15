from .common import *

DEBUG = bool(os.environ.get('DJANGO_DEBUG', True))


MIDDLEWARE += (
    'silk.middleware.SilkyMiddleware',
)

INSTALLED_APPS += (
    'silk',
)
