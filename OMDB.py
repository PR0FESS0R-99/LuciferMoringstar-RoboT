
import os
import requests

def get_movie_info(movieTitle):
    url = 'http://www.omdbapi.com'
    api_key = 'cce63883'
    data = {'apikey':api_key,'t':movieTitle}
    response = requests.get(url,data).json()

    if response.get("Response") != "True":
        return None

    movie_info = {}
    movie_info["title"] = response.get("Title")
    movie_info["year"] = response.get("Year")
    movie_info["release"] = response.get("Released")
    movie_info["duration"] = response.get("Runtime")
    movie_info["genre"] = response.get("Genre")
    movie_info["director"] = response.get("Director")
    movie_info["writer"] = response.get("Writer")
    movie_info["actors"] = response.get("Actors")
    movie_info["plot"] = response.get("Plot")
    movie_info["language"] = response.get("Language")
    movie_info["country"] = response.get("Country")
    movie_info["ratings"] = response.get("Ratings")
    movie_info["imdb_rating"] = response.get("imdbRating")
    movie_info["votes"] = response.get("imdbVotes")
    movie_info["imdb_id"] = response.get("imdbID")
    movie_info["box_office"] = response.get("box office")
    movie_info["pimage"] = response.get("Poster")

    return movie_info
