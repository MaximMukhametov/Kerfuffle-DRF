from django.db import models


class Contact(models.Model):
    """User contact information"""
    github = models.CharField(null=True, blank=True, max_length=100)
    vk = models.CharField(null=True, blank=True, max_length=100)
    facebook = models.CharField(null=True, blank=True, max_length=100)
    instagram = models.CharField(null=True, blank=True, max_length=100)
    twitter = models.CharField(null=True, blank=True, max_length=100)
    website = models.CharField(null=True, blank=True, max_length=100)
    youtube = models.CharField(null=True, blank=True, max_length=100)
    mainlink = models.CharField(null=True, blank=True, max_length=100)
