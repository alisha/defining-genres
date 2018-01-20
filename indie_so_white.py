import requests # to access the APIs
import json
import unicodecsv as csv
from pprint import PrettyPrinter
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

import secret # get API keys

# Definitions
LF_BASE = 'https://ws.audioscrobbler.com/2.0/'

# Authenticate spotify
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

features = ['danceability', 'energy', 'speechiness', 'tempo']
indie_artist_name = "Bjork"
possible_indie_artists = ["SZA", "FKA Twigs", "Dawn Richard"]

pp = PrettyPrinter(indent=2)

def write_artist_top_tracks_data(writer, artist):
  # Get data about the indie artist
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

def main():
  # Set up CSV file for pandas
  f = open('indie.csv', 'wb')
  writer = csv.writer(f, delimiter="|", quotechar="", quoting=csv.QUOTE_NONE, encoding='utf-8')
  writer.writerow(['artist name', 'song name'] + features)

  # Get data about all artists
  write_artist_top_tracks_data(writer, indie_artist_name)
  for artist in possible_indie_artists:
    write_artist_top_tracks_data(writer, artist)

  # Read data into pandas dataframe
  music_data = pd.read_csv('data.csv', sep='|', error_bad_lines=False)

  f.close()

if __name__ == '__main__':
  main()
