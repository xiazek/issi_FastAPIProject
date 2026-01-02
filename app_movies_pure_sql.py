from typing import Any
from fastapi import FastAPI
from movies_storage import MoviesStorage

app_movies_pure_sql = FastAPI()

@app_movies_pure_sql.get("/movies")
async def get_movies():
    movies_list = MoviesStorage.default().list()
    return movies_list

@app_movies_pure_sql.get('/movies/{movie_id}')
async def get_single_movie(movie_id:int):
    movie = MoviesStorage.default().find_by_id(movie_id)
    if movie is None:
        return {"message": "Movie not found"}
    return movie


@app_movies_pure_sql.post("/movies")
def add_movie(params: dict[str, Any]):
    ms = MoviesStorage.default()
    movie_id = ms.add_movie(params)
    return {"message": f"Movie added successfully. ID: {movie_id}", "movie_id": movie_id}


@app_movies_pure_sql.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    ms = MoviesStorage.default()
    ms.delete_movies_by_id([movie_id])
    return {"message": f"Movie with ID {movie_id} deleted successfully."}


@app_movies_pure_sql.delete("/movies")
def delete_movies(ids: list[int]):
    ms = MoviesStorage.default()
    count = ms.delete_movies_by_id(ids)
    return {"message": f"Deleted {count} movies."}


@app_movies_pure_sql.put("/movies/{movie_id}")
def update_movie(movie_id: int, params: dict[str, Any]):
    ms = MoviesStorage.default()
    updated = ms.update_movie(movie_id, params)
    if not updated:
        return {"message": "Movie not found"}
    return {"message": f"Movie with ID {movie_id} updated successfully."}
