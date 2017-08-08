import requests # to access the APIs
import json
from pprint import PrettyPrinter
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import secret # get API keys

LF_BASE = 'https://ws.audioscrobbler.com/2.0/'

pp = PrettyPrinter(indent=2)

genre = "indie" # for initial testing. TODO: test multiple genres

# get a genre's top artists
top_artists_params = {'method': 'tag.gettopartists', 'tag': genre, 'limit': 10, 'api_key': secret.LF_KEY, 'format': 'json'}
top_artists_request = requests.get(LF_BASE, params=top_artists_params).json()
top_artists = []
for artist in top_artists_request['topartists']['artist']:
  top_artists.append(artist['name'])

# authenticate spotify
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# for each artist, get top tracks from Spotify
top_tracks = []
genre_audio_features = {}
for artist in top_artists:
  artist_id = sp.search(artist, type="artist")["artists"]["items"][0]["id"]
  tracks = sp.artist_top_tracks(artist_id)["tracks"]
  for track in tracks:
    top_tracks.append(track["id"])

# get audio features for each track
audio_features = sp.audio_features(top_tracks)
danceability = []
energy = []
speechiness = []
tempo = []
for song in audio_features:
  danceability.append(song["danceability"])
  energy.append(song["energy"])
  speechiness.append(song["speechiness"])
  tempo.append(song["tempo"])

# create pandas DataFrames
danceability_obj = pd.DataFrame({'danceability' : pd.Series(danceability, index=top_tracks)})
energy_obj = pd.DataFrame({'energy' : pd.Series(energy, index=top_tracks)})
speechiness_obj = pd.DataFrame({'speechiness'  : pd.Series(speechiness, index=top_tracks)})
tempo_obj = pd.DataFrame({'tempo' : pd.Series(tempo, index=top_tracks)})

# display histograms
plt.figure()
danceability_obj.plot.hist()
energy_obj.plot.hist()
speechiness_obj.plot.hist()
tempo_obj.plot.hist()
plt.show(block=True)