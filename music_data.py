# Getting data
import requests # to access the APIs
import json
import unicodecsv as csv
from pprint import PrettyPrinter
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Analyzing data
import pandas as pd
import numpy as np
import scipy
from scipy.stats import ttest_ind

import secret # get API keys

# Definitions
LF_BASE = 'https://ws.audioscrobbler.com/2.0/'

# Authenticate spotify
client_credentials_manager = SpotifyClientCredentials(client_id=secret.SPOTIPY_CLIENT_ID, client_secret=secret.SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

features = ['danceability', 'energy', 'speechiness', 'tempo']

pp = PrettyPrinter(indent=2)


def write_artist_top_tracks_data(writer, artist):
  # Get data about the artist
  artist_data_params = {'method': 'artist.gettoptracks', 'artist': artist, 'limit': 10, 'api_key': secret.LF_KEY, 'format': 'json'}
  artist_data_request = requests.get(LF_BASE, params=artist_data_params).json()

  # For each track, get music data from spotify
  for track in artist_data_request['toptracks']['track']:
    song_name = track['name']
    audio_features = get_music_features(artist, song_name)
    if len(audio_features) > 0:
      write_to_csv(writer, artist, song_name, audio_features)


# Given a song and arist name, find that song on Spotify and return 
# an array of audio features for that song
def get_music_features(artist, song_name):
  q = 'artist:' + artist + " track:" + song_name
  sp_search = sp.search(q, type="track", limit=1)
  if len(sp_search['tracks']['items']) >= 1:
    song_id = sp_search['tracks']['items'][0]['id']
    
    # Get audio features
    audio_features = sp.audio_features(tracks=[song_id])
    song_features = []
    for feature in features:
      song_features.append(audio_features[0][feature])

    return song_features
  return []


# Given a CSV writer, artist name, song name, and an array of audio features,
# write that data to a CSV file
def write_to_csv(writer, artist, song_name, audio_features):
  writer.writerow([artist, song_name] + audio_features)


def get_data(csv_name, artists):
  # Set up CSV file for pandas
  f = open(csv_name, 'wb')
  writer = csv.writer(f, delimiter="|", quotechar="", quoting=csv.QUOTE_NONE, encoding='utf-8')
  writer.writerow(['artist', 'song'] + features)

  # Get data about all artists
  for artist in artists:
    write_artist_top_tracks_data(writer, artist)

  f.close()


def analyze_data(csv_name, definitely_indie_artists, possible_indie_artists):
  # Read data into pandas dataframe
  music_data = pd.read_csv(csv_name, sep='|', error_bad_lines=False)

  for artist in possible_indie_artists:
    for indie_artist in definitely_indie_artists:
      print("Comparing " + indie_artist + " and " + artist)
      num_diffs = 0

      indie_artist_df = music_data.query(('artist == "{}"').format(indie_artist))
      artist_df = music_data.query(('artist == "{}"').format(artist))

      for feature in features:
        # Print means
        indie_artist_avg = indie_artist_df[feature].mean()
        print(("Average {0} for {1} is {2}").format(feature, indie_artist, str(indie_artist_avg)))
        artist_avg = artist_df[feature].mean()
        print(("Average {0} for {1} is {2}").format(feature, artist, str(artist_avg)))

        # Do T-Test
        (stat, pvalue) = ttest_ind(indie_artist_df[feature], artist_df[feature])
        if pvalue < 0.05:
          num_diffs += 1
          print(("P value is {0}, so there is NO statistically significant difference\n").format(pvalue))
        else:
          print(("P value is {0}, so there IS a statistically significant difference\n").format(pvalue))

      print(("{0} and {1} differ in {2} out of {3} categories\n\n").format(indie_artist, artist, num_diffs, len(features)))