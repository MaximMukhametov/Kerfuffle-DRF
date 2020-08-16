from rest_framework.routers import DefaultRouter

from apps.dialogs.api.views import MessageModelViewSet


router = DefaultRouter()
router.register('message', MessageModelViewSet, basename='message')
urlpatterns = router.urls
