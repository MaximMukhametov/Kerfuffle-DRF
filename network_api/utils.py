from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.db.models.fields.files import ImageFieldFile


def get_resize_image(sourse_field: ImageFieldFile,
                     target_field: ImageFieldFile):
    small_photo = Image.open(sourse_field)
    small_photo.thumbnail((300, 300))
    thumb_io = BytesIO()
    small_photo.save(thumb_io, small_photo.format, quality=60)
    target_field.save(f'small{sourse_field.file.name}',
                      ContentFile(thumb_io.getvalue()), save=True)


class UserFields:
    user_show_fields = (
        'name', 'id', 'unique_url_name', 'photos', 'status')
    users_upload_field = ('name', 'id', 'unique_url_name', 'photos', 'status')
    profile_contacts_put_fields = (
        'id', 'looking_for_a_job', 'background_photo',
        'looking_for_a_job_description',
        'full_name',
        'contacts',)
    profile_contacts_get_fields = (
        'id', 'name', 'background_photo', 'looking_for_a_job',
        'looking_for_a_job_description',
        'full_name', 'posts',
        'contacts', 'photos')
    status_fields = ('status',)
    user_auth_fields = ('id', 'name', 'photos', 'background_photo')
