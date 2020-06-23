from django.contrib import admin

from network_api.models import User, Photo, Contact, Message, Post

admin.site.register([User, Photo, Contact, Message, Post])
