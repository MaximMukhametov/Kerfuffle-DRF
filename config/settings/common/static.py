import os

from config.settings.common.path import BASE_DIR

MEDIA_ROOT = os.path.join(BASE_DIR, '../../media')
MEDIA_URL = '/media/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
