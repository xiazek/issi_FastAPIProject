import os
from typing import Any

import requests
from fastapi import FastAPI

from movies_storage import MoviesStorage

debug = os.getenv("DEBUG") == "1"
app = FastAPI(debug=debug)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/sum")
async def calculate_sum(x: int = 0, y: int = 10):
    return x + y


@app.get("/geocode")
async def geocode(lat: float = 50.0680275, lon: float = 19.9098668):
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=jsonv2"

    headers = {
        # to imitate a real browser request
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }
    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code != 200:
        return {"error": f"Failed to fetch data, status code: {response.status_code}", "details": response.text}

    return response.json()["display_name"]

@app.get("/movies")
async def get_movies():
    movies_list = MoviesStorage.default().list()
    # output = []
    # for movie in movies:
    #     movie_dict = {
    #         "id": movie['id'],
    #         "title": movie['title'],
    #         "actors": movie['actors'],
    #     }
    #     output.append(movie_dict)
    # return output
    return movies_list

@app.get('/movies/{movie_id}')
async def get_single_movie(movie_id:int):
    movie = MoviesStorage.default().find_by_id(movie_id)
    if movie is None:
        return {"message": "Movie not found"}
    return MoviesStorage.default().find_by_id(movie_id)


@app.post("/movies")
def add_movie(params: dict[str, Any]):
    ms = MoviesStorage.default()
    movie_id = ms.add_movie(params)
    return {"message": f"Movie added successfully. ID: {movie_id}" }
