from django.urls import path

from apps.photos.api.views import PhotoUploadView

urlpatterns = [
    path('profile/photo/', PhotoUploadView.as_view(), name='profile'),
]
