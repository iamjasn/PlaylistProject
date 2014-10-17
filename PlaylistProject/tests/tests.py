from django.test import TestCase
from music_API.playlist_generator import Show, get_upcoming_shows, get_tracks

class ShowTestCase(TestCase):
    def setUp(self):
        Show.objects.create