from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.posts.api.views import LikeUnlikeView, PostView

router = DefaultRouter()
router.register('posts', PostView, basename='posts')

urlpatterns = [
    path('like/<int:pk>', LikeUnlikeView.as_view(), name='like'),
    path('', include(router.urls), name='post'),
]
