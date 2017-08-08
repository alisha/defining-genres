import requests # to access the APIs
import json
from pprint import PrettyPrinter
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

import secret # get API keys

LF_BASE = 'https://ws.audioscrobbler.com/2.0/'

pp = PrettyPrinter(indent=2)

genre = "indie" # for initial testing. TODO: test multiple genres

# get a genre's top artists
topArtistsParams = {'method': 'tag.gettopartists', 'tag': genre, 'limit': 1, 'api_key': secret.LF_KEY, 'format': 'json'}
topArtistsRequest = requests.get(LF_BASE, params=topArtistsParams).json()
topArtists = []
for artist in topArtistsRequest['topartists']['artist']:
  topArtists.append(artist['name'])

# authenticate spotify
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# for each artist, get top tracks from Spotify
topTracks = []
for artist in topArtists:
  print sp.search(artist, type="artist")
