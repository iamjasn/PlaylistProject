from django.shortcuts import render
from django import http
from django.http import HttpResponse, HttpRequest
from django.utils import timezone
import json
from datetime import date
from concert_preview.models import Playlist
from django.template import RequestContext
from django.shortcuts import render_to_response
from music_API.playlist_generator import get_tracks, get_upcoming_shows, convert_to_list, get_city
import pickle
import base64
from django.views.decorators.csrf import csrf_exempt
from api_keys import songkick_API


def get_shows(city, client_ip):
    try:
        shows_today = Playlist.objects.filter(
            date_generated=date.today(), metro_area__iexact=city)[0]
        # look for an existing record for today
        decoded_shows = base64.b64decode(shows_today.show_objects)
        shows = pickle.loads(decoded_shows)
        # from_cache = True
    except Playlist.DoesNotExist:
        # if nothing for today in this location:
        songkick_endpoint = 'http://api.songkick.com/api/3.0/' \
                                'events.json?apikey=%s&location=ip:%s&' \
                                'page=1' % str(songkick_API), str(client_ip)
        shows_today = get_upcoming_shows(songkick_endpoint)
        shows = get_tracks(shows_today)
        shows = convert_to_list(shows)
        pickled_shows = pickle.dumps(shows)
        encoded_shows = base64.b64encode(pickled_shows)
        Playlist.objects.create(date_generated=date.today(), metro_area=city,
                                show_objects=encoded_shows)
    return shows

def index(request):
    client_ip = request.META['REMOTE_ADDR']
    context = RequestContext(request)
    city = get_city(client_ip)
    shows = get_shows(city, client_ip)
    context_dict = {'shows': shows, 'city': city}
    return render_to_response('concert_preview/index.html', context_dict, context)

def data(request):
    client_ip = request.META['REMOTE_ADDR']
    city = get_city(client_ip)
    shows = get_shows(city, client_ip)
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
