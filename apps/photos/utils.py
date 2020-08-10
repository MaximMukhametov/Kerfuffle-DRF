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
