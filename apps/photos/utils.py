from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.db.models.fields.files import ImageFieldFile


def get_resize_image(source_field: ImageFieldFile,
                     target_field: ImageFieldFile) -> None:
    """
    Gets an image and creates a thumbnail copy of it.

    Parameters
    ----------
    source_field: is a model field that stores a larger image
    target_field: is a model field that stores a smaller image
    """

    small_photo = Image.open(source_field)
    small_photo.thumbnail((300, 300))

    # A stream implementation using an in-memory bytes buffer,
    # this is necessary to save the thumbnail in memory
    thumb_io = BytesIO()
    small_photo.save(thumb_io, small_photo.format, quality=60)
    target_field.save(f'small{source_field.file.name}',
                      ContentFile(thumb_io.getvalue()), save=True)
