from django.shortcuts import render
from django import http
from django.http import HttpResponse
from django.utils import timezone
import json
from datetime import date
from gen_playlists.models import Playlist
from django.template import RequestContext
from django.shortcuts import render_to_response
from music_API.playlist_generator import get_tracks, get_upcoming_shows, convert_to_array, get_city
import pickle
import base64

def get_shows(city):

    try:
        shows_today = Playlist.objects.get(date_generated=date.today(), metro_area__iexact=city)
        # look for an existing record for today
        decoded_shows = base64.b64decode(shows_today.show_objects)
        shows = pickle.loads(decoded_shows)

    except Playlist.DoesNotExist:
        # if nothing for today in this location:
        shows_today = get_upcoming_shows()
        shows = get_tracks(shows_today)
        shows = convert_to_array(shows)
        pickled_shows = pickle.dumps(shows)
        encoded_shows = base64.b64encode(pickled_shows)
        Playlist.objects.create(date_generated=date.today(), metro_area=city,
                                  show_objects=encoded_shows)
    return shows

def index(request):
    context = RequestContext(request)
    city = get_city()
    shows = get_shows(city)

    context_dict = { 'shows': shows, 'city': city }
    return render_to_response('gen_playlists/index.html', context_dict, context)

def data(request):
    city = get_city()
    shows = get_shows(city)
    show_list = []
    for show in shows:
        item = {}
        item['display_name'] = show.sk_display_name
        item['artist'] = show.artist
        item['uri'] = show.event_uri
        item['track'] = show.track
        item['bio'] = show.bio
        item['bio_link'] = show.bio_link
        item['genre'] = show.genre
        item['image'] = show.image
        show_list.append(item)
    json_data = json.dumps(show_list)
    return http.HttpResponse(json_data, content_type='text/json')

def home(request):
    context = RequestContext(request)
    city = get_city()
    shows = get_shows(city)

    context_dict = { 'shows': shows, 'city': city }
    return render_to_response('gen_playlists/home.html', context_dict, context)