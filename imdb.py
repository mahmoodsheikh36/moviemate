import requests
import json
from urllib.parse import quote

from movie import Movie

def search(movie_name):
    r = requests.get('https://v2.sg.media-imdb.com/suggestion/{}/{}.json'.format(
        movie_name[0],
        quote(movie_name)
    ))
    r_json = json.loads(r.text)
    movies = []
    for r_movie in r_json['d']:
        if 'y' in r_movie:
            movies.append(Movie(r_movie['l'], r_movie['y'], r_movie['i']['imageUrl']))
        else:
            movies.append(Movie(r_movie['l'], 0, r_movie['i']['imageUrl']))
    return movies
