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
import music_data

# Inspiration: https://newrepublic.com/article/121437/why-indie-music-so-unbearably-white

def main():

  # definitely_indie_artists = ["Bjork"]
  # possible_indie_artists = ["SZA", "FKA Twigs", "Dawn Richard"]
  # artists = definitely_indie_artists + possible_indie_artists

  definitely_indie_artists = ["Dirty Projectors", "Vampire Weekend"]
  possible_indie_artists = ["Valerie June"]
  artists = definitely_indie_artists + possible_indie_artists

  #music_data.get_data(artists)
  music_data.analyze_data("indie.csv", definitely_indie_artists, possible_indie_artists)


if __name__ == '__main__':
  main()
