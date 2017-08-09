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

genres = ['indie'] #, 'pop', 'rap', 'country'
features = ['danceability', 'energy', 'speechiness', 'tempo']

# authenticate spotify
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

f = open('data.csv', 'w')
f.write('genre, artist name, song name, ')
f.write(', '.join(features))
f.write('\n')

for genre in genres:
  # get a genre's top artists
  top_artists_params = {'method': 'tag.gettopartists', 'tag': genre, 'limit': 1, 'api_key': secret.LF_KEY, 'format': 'json'}
  top_artists_request = requests.get(LF_BASE, params=top_artists_params).json()
  top_artists = []
  for artist in top_artists_request['topartists']['artist']:
    top_artists.append(artist['name'])

  # for each artist, get top tracks from Spotify
  for artist in top_artists:
    artist_id = sp.search(artist, type="artist")["artists"]["items"][0]["id"]
    tracks = sp.artist_top_tracks(artist_id)["tracks"]
    
    # create new CSV entry for each song, put audio features
    for track in tracks:
      f.write(genre + ', ' + track['artists'][0]['name'] + ', ' + track['name'] + ', ')
      audio_features = sp.audio_features([track["id"]])
      song_features = []
      for feature in features:
        song_features.append(audio_features[0][feature])
      f.write(', '.join(str(val) for val in song_features))
      f.write('\n')

f.close()

# pandas

'''danceability_obj = pd.DataFrame(danceability)
plt.figure()
danceability_obj.plot.hist(alpha=0.5, title="Danceability of hit songs for various genres")
plt.show(block=True)

# create pandas DataFrames
danceability_obj = pd.DataFrame(danceability)
energy_obj = pd.DataFrame({'energy' : pd.Series(energy, index=top_tracks)})
speechiness_obj = pd.DataFrame({'speechiness'  : pd.Series(speechiness, index=top_tracks)})
tempo_obj = pd.DataFrame({'tempo' : pd.Series(tempo, index=top_tracks)})

# display histograms
plt.figure()
danceability_obj.plot.hist()
energy_obj.plot.hist()
speechiness_obj.plot.hist()
tempo_obj.plot.hist()
plt.show(block=True)'''