from django.contrib import admin

# Register your models here.
from .models import PhotoAlbum,Photos
admin.site.register(PhotoAlbum)
admin.site.register(Photos)