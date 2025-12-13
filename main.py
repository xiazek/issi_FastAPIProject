import requests

from fastapi import FastAPI

from movies_storage import MoviesStorage

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello Wo2122211rld1221"}


@app.get("/sum")
async def sum(x: int = 0, y: int = 10):
    return x + y


@app.get("/geocode")
async def geocode(lat: float = 50.0680275, lon: float = 19.9098668):
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=jsonv2"

    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    return response.json()["display_name"]
    # return {"lat": lat, "lon": lon}


@app.get("/movies")
async def movies():
    movies = MoviesStorage.default().list()
    # output = []
    # for movie in movies:
    #     movie_dict = {
    #         "id": movie['id'],
    #         "title": movie['title'],
    #         "actors": movie['actors'],
    #     }
    #     output.append(movie_dict)
    # return output
    return movies

@app.get('/movies/{movie_id}')
def get_single_movie(movie_id:int):
    movie = MoviesStorage.default().find_by_id(movie_id)
    if movie is None:
        return {"message": "Movie not found"}
    return MoviesStorage.default().find_by_id(movie_id)

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
