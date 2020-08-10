from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.photos.api.serializers import PhotosSerializer, PhotosUploadSerializer
from apps.photos.models.photo import Photo


class PhotoUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        photo = Photo.objects.get(user=request.user.id)
        serializer = PhotosSerializer(photo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):

        photo_serializer = PhotosUploadSerializer(data=request.data)

        if photo_serializer.is_valid():
            photo_serializer.save(user=request.user)
            response_serializer = PhotosSerializer(photo_serializer.instance)
            return Response(response_serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(photo_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
