from django.db import models

# Create your models here.
class Playlist(models.Model):
    shows_location = models.CharField(max_length=200)
    date_generated = models.DateTimeField('generated on')

class User(models.Model):
    user_name = models.CharField(max_length=200)