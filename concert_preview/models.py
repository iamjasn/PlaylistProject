from django.db import models

class Playlist(models.Model):
    date_generated = models.DateField()
    metro_area = models.CharField(max_length=255)
    show_objects = models.TextField()