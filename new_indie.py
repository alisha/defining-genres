import music_data

potential_indie_artists = ["SZA", "FKA Twigs", "Dawn Richard", "Valerie June", "M.I.A."]

# artists = music_data.get_similar_artists("Vampire Weekend")
# print(artists)

print(music_data.get_genre_top_artists("indie", num_artists=2))