from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.dialogs.api.views import MessageModelViewSet
from apps.photos.api.views import PhotoUploadView
from apps.posts.api.views import PostView, LikeUnlikeView
from apps.users.api.views import UsersTotalAPI, UserProfileView, \
    UserAuthView, FollowUnfollowView
from .settings.development import DEBUG
from config.swagger import urlpatterns as docs_api_urls

router = DefaultRouter()
router.register('posts', PostView, basename='posts')
router.register('users', UsersTotalAPI, basename='users')
router.register('profile', UserProfileView, basename='profile')
router.register('auth/me', UserAuthView, basename='auth')
router.register('message', MessageModelViewSet, basename='message')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/photo/', PhotoUploadView.as_view(), name='profile'),
    path('auth/', include('djoser.urls.jwt'), name='djoser.urls.jwt'),
    path('', include(router.urls), name='message'),
    path('follow/<int:pk>', FollowUnfollowView.as_view(), name='follow'),
    path('like/<int:pk>', LikeUnlikeView.as_view(), name='like'),

]

# swagger urls
urlpatterns += docs_api_urls

if DEBUG:
    urlpatterns += [url(r'^silk/', include('silk.urls', namespace='silk'))]
