INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'corsheaders'
]

LOCAL_APPS = [
    'apps.users',
    'apps.contacts',
    'apps.dialogs',
    'apps.photos',
    'apps.posts',

]

INSTALLED_APPS += LOCAL_APPS
