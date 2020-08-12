from .authentication import *
from .cors import *
from .databases import *
from .drf import *
from .installed_apps import *
from .internationalization import *
from .jwt import *
from .middleware import *
from .notifications import *
from .path import *
from .security import *
from .static import *
from .storage import *
from .templates import *


ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

DATETIME_FORMAT = "%m/%d/%Y %H:%M:%S"
