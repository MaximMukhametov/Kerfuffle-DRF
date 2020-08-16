from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.posts.api.views import PostView
from config.swagger import urlpatterns as docs_api_urls
from .settings.development import DEBUG

router = DefaultRouter()
router.register('posts', PostView, basename='posts')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.users.api.urls')),
    path('api/v1/', include('apps.dialogs.api.urls')),
    path('api/v1/', include('apps.photos.api.urls')),
    path('api/v1/', include('apps.posts.api.urls')),
    path('auth/', include('djoser.urls.jwt'), name='djoser.urls.jwt'),
]

# swagger urls
urlpatterns += docs_api_urls

if DEBUG:
    urlpatterns += [url(r'^silk/', include('silk.urls', namespace='silk'))]
