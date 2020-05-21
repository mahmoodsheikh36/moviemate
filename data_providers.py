import requests
import json
from urllib.parse import quote

from movie import Movie
from config import Config

class OMDbClient:
    def __init__(self, apikey=Config.omdb_apikey):
        self.apikey = apikey

    def search(self, query):
        url = 'http://www.omdbapi.com/?apikey={}&s={}&type=movie'.format(
            self.apikey,
            quote(query)
        )
        r = requests.get(url)
        r_json = json.loads(r.text)
        if not 'Search' in r_json:
            return []
        movies = []
        for r_movie in r_json['Search']:
            movie = Movie(r_movie['Title'], r_movie['Year'], r_movie['Poster'])
            movies.append(movie)
        return movies

class IMDBClient:
    def __init__(self):
        pass

    def search(self, query):
        r = requests.get('https://v2.sg.media-imdb.com/suggestion/{}/{}.json'.format(
            movie_name[0],
            quote(movie_name)
        ))
        r_json = json.loads(r.text)
        movies = []
        for r_movie in r_json['d']:
            poster = r_movie['i']['imageUrl']
            small_poster = poster.replace('_V1_.jpg', '_V1_UY148_CR8,0,100,148_.jpg')
            if 'y' in r_movie:
                movies.append(Movie(r_movie['l'], r_movie['y'], poster, small_poster))
            else:
                movies.append(Movie(r_movie['l'], 0, poster, small_poster))
        return movies

