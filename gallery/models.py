from django.db import models
from taggit.managers import TaggableManager


# Create your models here.
class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    tags = TaggableManager()    
