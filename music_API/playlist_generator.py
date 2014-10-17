from urllib import urlopen
import json
from rdio import Rdio
from api_keys import songkick_api, rdio, echo_nest_api_start, echo_nest_api_end


"""A collection of functions for getting data from 
Songkick and Rdio."""


def get_city():
    # display location separately on page 
    results = urlopen('http://freegeoip.net/json/')
    raw = results.read()
    response = json.loads(raw)
    if response:
        city = "%s, %s" % (response['city'], response['region_code'])
    else:
        city = None
    return city

class Show(object):
    def __init__(self, artist_id, artist, venue, city, when, event_uri, track, sk_display_name, genre, bio,
                 bio_link, image):
        self.artist_id = artist_id
        self.artist = artist
        self.venue = venue
        self.city = city
        self.when  = when
        self.event_uri = event_uri
        self.track = track
        self.sk_display_name = sk_display_name
        self.genre = genre
        self.bio = bio
        self.bio_link = bio_link
        self.image = image

def make_new_show(event):
    artist_id = event['performance'][0]['artist']['id']
    artist = event['performance'][0]['displayName']
    venue = event['venue']['displayName']
    city = event['location']['city']
    when = event['start']['date']
    event_uri = event['uri']
    track = ""
    sk_display_name = event['displayName']
    genre = "genre unknown"
    bio = ""
    bio_link = ""
    image = ""
    # for each Songkick event in event_list, new Show object
    show = Show(artist_id, artist, venue, city, when, event_uri, track, sk_display_name, genre, bio, bio_link, image)
    return show

def get_upcoming_shows():
    # retrieve events from Songkick
    upcoming_shows = {}
    results = urlopen(songkick_api)
    raw = results.read()
    response = json.loads(raw)
    events = response['resultsPage']['results']['event']
    for event in events:
        if event['status'] != 'cancelled':
            show = make_new_show(event)
            upcoming_shows[show.artist] = show
    return upcoming_shows

def get_tracks(upcoming_shows):
    for k,v in upcoming_shows.items():
        show = v
        # get rdio id from echo nest api
        endpoint = echo_nest_api_start + str(show.artist_id) + echo_nest_api_end
        results = urlopen(endpoint)
        raw = results.read()
        response = json.loads(raw)
        # make sure rdio id exists in echo nest
        if response['response']['status']['message'] != "The Identifier specified does not exist":
            if 'foreign_ids' in response['response']['artist']:
                rdio_artist = response['response']['artist']['foreign_ids'][0]['foreign_id']
                # truncate rdio id to be usable
                foreign_id = rdio_artist.split(':')
                rdio_artist = foreign_id[2]
                show.artist_id = rdio_artist
                rdio_response = rdio.call('getTracksForArtist', {'artist': show.artist_id })
                if rdio_response['result']:
                    show.track = rdio_response['result'][0]['embedUrl']
                if response['response']['artist']['genres']:
                    show.genre = response['response']['artist']['genres'][0]['name']
                if response['response']['artist']['biographies']:
                    bios_list = response['response']['artist']['biographies']
                    # use wikipedia link if available
                    for i in range(len(bios_list)):
                        if bios_list[0]['site'] == 'last.fm':
                            show.bio = bios_list[0]['text']
                            show.bio_link = bios_list[0]['url']
                        else:
                            show.bio = bios_list[0]['text']
                            show.bio_link = bios_list[0]['url']
                if response['response']['artist']['images']:
                    show.image = response['response']['artist']['images'][0]['url']
            else:
                show.track = ""
        else:
            show.track = ""
    return upcoming_shows

def list_shows(upcoming_shows):
    # convert dict to array and sort by date
    shows_list = []
    for k,v in upcoming_shows.items():
        shows_list.append(v)
    for show in shows_list:
        if not show.track:
            shows_list.remove(show)
    shows_list.sort(key=lambda x: x.when, reverse=False)
    return shows_list