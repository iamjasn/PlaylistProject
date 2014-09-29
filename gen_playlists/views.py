from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from music_API.playlist_generator import get_tracks, get_upcoming_shows, convert_to_array

# Create your views here.
def index(request):
    context = RequestContext(request)
    shows = get_upcoming_shows()
    shows = get_tracks(shows)
    shows = convert_to_array(shows)
    # p = Profile()
    # profile_dict = {'city': p.city}
    context_dict = {'shows': shows }
    return render_to_response('gen_playlists/index.html', context_dict, context)
