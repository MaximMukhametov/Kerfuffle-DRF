from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.users.api.views import (
    UsersTotalAPI,
    UserProfileView,
    UserAuthView,
    FollowUnfollowView
)

router = DefaultRouter()
router.register('users', UsersTotalAPI, basename='users')
router.register('profile', UserProfileView, basename='profile')
router.register('auth/me', UserAuthView, basename='auth')
urlpatterns = [
    path('follow/<int:pk>', FollowUnfollowView.as_view(), name='follow'),
    path('', include(router.urls), name='message'),
]
