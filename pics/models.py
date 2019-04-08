from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.urls import reverse


class PhotoAlbum(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    Name = models.CharField(max_length=100,verbose_name='Name of the album')

    def get_absolute_url(self):
        success_url = reverse('pics:detail', kwargs={'pk': self.pk})
        return success_url

    def __str__(self):
        return self.Name

class Photos(models.Model):
    Album = models.ForeignKey(PhotoAlbum,on_delete=models.CASCADE)
    caption = models.CharField(max_length=20)
    needs_edit = models.CharField(choices=[('yes','yes'),('no','no')],max_length=20)
    image = models.FileField()

    def __str__(self):
        return self.caption

    def get_absolute_url(self):
        success_url = reverse('pics:detail_photos', kwargs={'pk': self.pk})
        return success_url
