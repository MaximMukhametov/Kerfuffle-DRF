from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.photos.api.views import PhotoUploadView
from apps.posts.api.views import PostView, LikeUnlikeView
from config.swagger import urlpatterns as docs_api_urls
from .settings.development import DEBUG

router = DefaultRouter()
router.register('posts', PostView, basename='posts')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.users.api.urls')),
    path('api/v1/', include('apps.dialogs.api.urls')),

    path('profile/photo/', PhotoUploadView.as_view(), name='profile'),
    path('auth/', include('djoser.urls.jwt'), name='djoser.urls.jwt'),
    path('like/<int:pk>', LikeUnlikeView.as_view(), name='like'),

]

# swagger urls
urlpatterns += docs_api_urls

if DEBUG:
    urlpatterns += [url(r'^silk/', include('silk.urls', namespace='silk'))]
