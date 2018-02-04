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
from pathlib import Path

import secret # get API keys

# Definitions
LF_BASE = 'https://ws.audioscrobbler.com/2.0/'

# Authenticate spotify
client_credentials_manager = SpotifyClientCredentials(client_id=secret.SPOTIPY_CLIENT_ID, client_secret=secret.SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

features = ['danceability', 'energy', 'speechiness', 'tempo']

pp = PrettyPrinter(indent=2)

# Returns an array of similar artists using Last.fm API
def get_similar_artists(artist, num_artists=10):
  similar_artists_params = {'method': 'artist.getSimilar', 'artist': artist, 'limit': num_artists, 'api_key': secret.LF_KEY, 'format': 'json'}
  similar_artists_request = requests.get(LF_BASE, params=similar_artists_params).json()

  similar_artists = []

  # pp.pprint(similar_artists_request["similarartists"]["artist"])
  for artist in similar_artists_request["similarartists"]["artist"]:
    similar_artists.append(artist["name"])

  return similar_artists


def get_genre_top_artists(genre, num_artists=10):
  # Get a genre's top artists
  top_artists_params = {'method': 'tag.gettopartists', 'tag': genre, 'limit': num_artists, 'api_key': secret.LF_KEY, 'format': 'json'}
  top_artists_request = requests.get(LF_BASE, params=top_artists_params).json()

  top_artists = []

  for artist in top_artists_request["topartists"]["artist"]:
    top_artists.append(artist["name"])

  return top_artists


# Writes artist's top tracks to the CSV defined by the writer
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


def compare_two_artists(artist1_name, artist1_df, artist2_name, artist2_df, features):
  num_diffs = 0

  for feature in features:
    # Print means
    artist1_avg = artist1_df[feature].mean()
    print(("Average {0} for {1} is {2}").format(feature, artist1_name, str(artist1_avg)))
    artist_avg = artist2_df[feature].mean()
    print(("Average {0} for {1} is {2}").format(feature, artist2_name, str(artist_avg)))

    # Do T-Test
    (stat, pvalue) = ttest_ind(artist1_df[feature], artist2_df[feature])
    if pvalue < 0.05:
      num_diffs += 1
      print(("P value is {0}, so there is NO statistically significant difference\n").format(pvalue))
    else:
      print(("P value is {0}, so there IS a statistically significant difference\n").format(pvalue))

  print(("{0} and {1} differ in {2} out of {3} categories\n\n").format(artist1_name, artist2_name, num_diffs, len(features)))


# Analyzes data in csv_name, so assumes data has already been retrieved
# Compares the artists in group1 with the artists in group2
def analyze_data(csv_name, group1, group2):
  # Make sure that the csv file exists
  if not Path(csv_name).is_file():
    print("Cannot access {0}", csv_name)
    return

  # Read data into pandas dataframe
  music_data = pd.read_csv(csv_name, sep='|', error_bad_lines=False)

  for artist1 in group1:
    for artist2 in group2:
      print("Comparing " + artist1 + " and " + artist2)

      artist1_df = music_data.query(('artist == "{}"').format(artist1))
      artist2_df = music_data.query(('artist == "{}"').format(artist2))
      compare_two_artists(artist1, artist1_df, artist2, artist2_df, features)

      