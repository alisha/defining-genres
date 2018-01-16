import requests # to access the APIs
import json
import unicodecsv as csv
from pprint import PrettyPrinter
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

import secret # get API keys

LF_BASE = 'https://ws.audioscrobbler.com/2.0/'

pp = PrettyPrinter(indent=2)

genres = ['indie', 'pop', 'rap', 'country']
features = ['danceability', 'energy', 'speechiness', 'tempo']

# Authenticate spotify
client_credentials_manager = SpotifyClientCredentials(client_id=secret.SPOTIPY_CLIENT_ID, client_secret=secret.SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

f = open('data.csv', 'wb')
writer = csv.writer(f, delimiter="|", quotechar="", quoting=csv.QUOTE_NONE, encoding='utf-8')
writer.writerow(['genre', 'artist name', 'song name'] + features)

for genre in genres:
  # Get a genre's top tracks
  top_tracks_params = {'method': 'tag.gettoptracks', 'tag': genre, 'limit': 50, 'api_key': secret.LF_KEY, 'format': 'json'}
  top_tracks_request = requests.get(LF_BASE, params=top_tracks_params).json()

  # For each track, get music data from spotify
  for track in top_tracks_request['tracks']['track']:
    song_name = track['name']
    artist = track['artist']['name']
    
    # Find song on Spotify
    q = 'artist:' + artist + " track:" + song_name
    sp_search = sp.search(q, type="track", limit=1)
    if len(sp_search['tracks']['items']) >= 1:
      song_id = sp_search['tracks']['items'][0]['id']
      
      # Get audio features
      audio_features = sp.audio_features(tracks=[song_id])
      song_features = []
      for feature in features:
        song_features.append(audio_features[0][feature])

      # Write to CSV file
      writer.writerow([genre, artist, song_name] + song_features)

f.close()
