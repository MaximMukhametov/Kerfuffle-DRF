from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from network_api.views import UsersTotalAPI, UserProfileView, \
    UserStatusView, \
    PhotoUploadView, UserAuthView, MessageView, PostView, FollowUnfollowView, \
    LikeUnlikeView
from .settings import DEBUG

router = DefaultRouter()
router.register('posts', PostView, basename='posts')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', UsersTotalAPI.as_view(), name='users'),
    path('profile/status/', UserStatusView.as_view(), name='users'),
    path('profile/status/<int:pk>', UserStatusView.as_view(), name='users'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/<int:pk>', UserProfileView.as_view(), name='profile'),
    path('profile/photo/', PhotoUploadView.as_view(), name='profile'),
    path('auth/', include('djoser.urls.jwt'), name='djoser.urls.jwt'),
    path('auth/me/', UserAuthView.as_view(), name='authme'),
    path('message/<int:pk>', MessageView.as_view(), name='message'),
    path('', include(router.urls), name='message'),
    path('follow/<int:pk>', FollowUnfollowView.as_view(), name='follow'),
    path('like/<int:pk>', LikeUnlikeView.as_view(), name='like'),

]

if DEBUG:
    urlpatterns += [url(r'^silk/', include('silk.urls', namespace='silk'))]
