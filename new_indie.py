import music_data

# Get artists
potential_indie_artists_seed = ["SZA", "FKA Twigs", "Dawn Richard", "Valerie June", "M.I.A."]
potential_indie_artists = potential_indie_artists_seed
for artist in potential_indie_artists_seed:
  similar_artists = music_data.get_similar_artists(artist, num_artists=1)
  for similar_artist in similar_artists:
    if similar_artist not in potential_indie_artists:
      potential_indie_artists.append(similar_artist)

definite_indie_artists = music_data.get_genre_top_artists("indie", num_artists=len(potential_indie_artists))

all_artists = potential_indie_artists + definite_indie_artists

# Compare all artists
# music_data.get_data("similar_indie.csv", all_artists)
music_data.analyze_data("similar_indie.csv", potential_indie_artists, definite_indie_artists, "similar_indie.txt")
