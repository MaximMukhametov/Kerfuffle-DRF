from django.db import models

__all__ = (
    'Photo',
)


class Photo(models.Model):
    """User photo."""
    small_img = models.ImageField(null=True, blank=True,
                                  verbose_name='Small img')
    large_img = models.ImageField(null=True, blank=True,
                                  verbose_name='Large img')
