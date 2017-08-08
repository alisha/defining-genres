# Defining Genres

## Goals

Music genres are difficult to define. This project attempts to identify the primarcy characteristics of various genres using data from the Spotify API.

## Roadmap/TODOs

* Create list of genres to test
* For a given genre, find the top artists (exact number TBD)
  * Will probably use the last.fm API for this
* For a given artist, find their top songs (exact number TBD)
* For a given song, find its ["audio features"](https://developer.spotify.com/web-api/get-audio-features/) from the Spotify API
* Determine the mean and medians of the audio features for each genre's hit songs
* Compare those means and medians for various genres

### Future improvements

* Weight artists and songs by popularity (e.g. the genre's most popular artist will "count" more than a less popular artist)
