from django.db import models


class Photo(models.Model):
    """User photo"""
    small = models.TextField(null=True, blank=True,
                             verbose_name='Small',
                             help_text='This field with a link to '
                                       'the small size photo for users '
                                       'downloaded from a third-party API')
    small_img = models.ImageField(null=True, blank=True,
                                  verbose_name='Small img')
    large = models.TextField(null=True, blank=True, verbose_name='Large',
                             help_text='This field with a link to '
                                       'the large size photo for users '
                                       'downloaded from a third-party API')
    large_img = models.ImageField(null=True, blank=True,
                                  verbose_name='Large img')
