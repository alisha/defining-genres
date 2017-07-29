import requests # to access the APIs
import secret # get API keys

LF_BASE = 'https://ws.audioscrobbler.com/2.0/'

genre = "indie" # for initial testing. TODO: test multiple genres

# get a genre's top artists
getGenreParams = {'method': 'tag.gettopartists', 'tag': genre, 'limit': 5, 'api_key': secret.LF_KEY, 'format': 'json'}
r = requests.get(LF_BASE, params=getGenreParams)
print r.text