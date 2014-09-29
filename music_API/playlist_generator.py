from urllib import urlencode, urlopen, quote_plus
import json
from rdio import Rdio
from api_keys import songkick_api, rdio, echo_nest_api_start, echo_nest_api_end
# from pprint import pprint

"""A collection of functions for getting data from 
Songkick and Rdio."""


user_country = 'US'


class Profile(object):
    def __init__(self):
        self.get_city()
    def get_city(self):
        results = urlopen('http://freegeoip.net/json/')
        raw = results.read()
        response = json.loads(raw)
        if response:
            self.city = response['city']
        else:
            self.city = None

# def truncate_to_300(text):
#     if len(text) <= 300:
#         return text
#     else:
#         return text[:300] + '...'




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
    #formatting
    # city = city.split(",")
    # city = city[0]
    #
    # when = when.split("-")
    # when.pop(0)
    # when = "/".join(when)
    #
    # if venue == 'Unknown venue':
    #     venue = 'See band website for venue'

    # for each Songkick event in event_list, new Show object
    show = Show(artist_id, artist, venue, city, when, event_uri, track, sk_display_name, genre, bio, bio_link, image)
    return show


def get_upcoming_shows():
    upcoming_shows = {}
    results = urlopen(songkick_api)
    raw = results.read()
    response = json.loads(raw)
    events = response['resultsPage']['results']['event']
    for event in events:
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
        # make sure songkick id exists in echo nest
        if response['response']['status']['message'] != "The Identifier specified does not exist":
            if 'foreign_ids' in response['response']['artist']:
                rdio_artist = response['response']['artist']['foreign_ids'][0]['foreign_id']
                # truncate rdio id to be usable
                foreign_id = rdio_artist.split(':')
                rdio_artist = foreign_id[2]
                show.artist_id = rdio_artist
                rdio_response = rdio.call('getTracksForArtist', {'artist': show.artist_id })
                show.track = rdio_response['result'][0]['embedUrl']
                if response['response']['artist']['genres']:
                    show.genre = response['response']['artist']['genres'][0]['name']
                if response['response']['artist']['biographies']:
                    show.bio = response['response']['artist']['biographies'][0]['text']
                    show.bio_link = response['response']['artist']['biographies'][0]['url']
                if response['response']['artist']['images']:
                    show.image = response['response']['artist']['images'][0]['url']
            else:
                show.track = ""
        else:
            show.track = ""
    return upcoming_shows

def convert_to_array(upcoming_shows):
    shows_list = []
    for k,v in upcoming_shows.items():
        shows_list.append(v)
    shows_list.sort(key=lambda x: x.when, reverse=False)
    return shows_list


# def get_bio(upcoming_shows):
#     for show in upcoming_shows:
#         endpoint = 'http://developer.echonest.com/api/v4/artist/biographies?api_key=59QM9FSJQ2HBN8N7P&id=rdio:artist' \
#                    ':' + show.artist_id + '&format=json&results=1&start=0&license=cc-by-sa'
#         results = urlopen(endpoint)
#         raw = results.read()
#         response = json.loads(raw)
#         if response['response']['status']['biographies']:
#             bio = response['response']['status']['biographies']['text']
#             show.bio = truncate(bio, 300)

# get_upcoming_shows(songkick_api)


# def display_upcoming_shows(upcoming_shows_list):
#     for show in upcoming_shows:
#         print "%s %s %s %s" % (show.artist, show.venue, show.city, show.when)


# display_upcoming_shows(upcoming_shows)


# def get_spotify_tracks(upcoming_shows):
#     # print len(upcoming_shows)
#     for show in upcoming_shows:
#         artist_url = "https://api.spotify.com/v1/search?q=%s&type=artist" % quote_plus(show.artist)
#         results = urlopen(artist_url)
#         raw = results.read()
#         response = json.loads(raw)
#         artists = response['artists']
#         items = artists['items']
#
#         if items:
#             artist = items[0]
#             spotify_artist_id = artist['id']
#             get_track_url = "https://api.spotify.com/v1/artists/%s/top-tracks?country=%s" % (spotify_artist_id, user_country)
#             artist_results = urlopen(get_track_url)
#             artist_raw = artist_results.read()
#             response2 = json.loads(artist_raw)
#             if response2['tracks']:
#                 show.track = response2['tracks'][0]['uri']
#             else:
#                 show.track = None
#         else:
#             show.track = None
#     return upcoming_shows


# if response['artists']['items']:
#     headliner = response['artists']['items'][0]
#     spotify_name = headliner['name']
#     genres = response['artists']['items'][0]['genres']
#     spotify_artist_id = response['artists']['items'][0]['id']
#     main_image = response['artists']['items'][0]['images']
#     if main_image:
#         main_image = main_image[1]['url']
#     else:
#         main_image = 'image unavailable'
#     if genres:
#         genres = genres[0]
#     else:
#         genres = 'no genre available'
#     # print "%s - %s - %s - %s - %s" % (show.artist, spotify_name, genres, spotify_artist_id, main_image)
#
#     get_track_url = "https://api.spotify.com/v1/artists/%s/top-tracks?country=%s" % (spotify_artist_id, user_country)
#     results = urlopen(get_track_url)
#     raw = results.read()
#     response = json.loads(raw)
#     # pprint(response)
#     # top_track_id = response['tracks'][0]['id']
#     # top_track_name = response['tracks'][0]['name']
#     if response['tracks']:
#         top_track_uri = response['tracks'][0]['uri']
#         show.track = response['tracks']
#     # print "Top track %s has the id %s" % (top_track_name, top_track_id)
#     # print 'uri: ' + top_track_uri
#         #print "%s %s %s %s" % (show.artist, show.venue, show.city, show.when)
#         #print "%s %s" % (genres, main_image)
#
#         return "<iframe src='https://embed.spotify.com/?uri=%s' width='250' height='80' frameborder='0' allowtransparency='true'></iframe>" % 'top_track_uri'
#
#     else:
#         # print "%s %s %s %s" % (show.artist, show.venue, show.city, show.when)
#         # print "%s %s" % (genres, main_image)
#         return "Sorry, this artist's spotify tracks are not available in your country."
#
# else:
#     return "Sorry, %s is not in the spotify catalogue." % show.artist

# get_spotify_tracks(upcoming_shows)




