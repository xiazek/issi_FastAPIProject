# ORM version
from typing import Any

from fastapi import FastAPI
from playhouse.shortcuts import model_to_dict

from orm_models import Actor, Movie

app_movies_orm = FastAPI()

@app_movies_orm.get("/movies")
async def get_orm_movies():
    movies_list = list(Movie.select().dicts())
    return movies_list

@app_movies_orm.get("/movies/{movie_id}")
async def get_orm_single_movie(movie_id:int):
    movie = Movie.get_or_none(Movie.id == movie_id)
    if movie is None:
        return {"message": "Movie not found"}
    return model_to_dict(movie)

@app_movies_orm.get("/movies/{movie_id}/actors")
async def get_actors_for_movie(movie_id:int):
    movie = Movie.get_or_none(Movie.id == movie_id)
    if movie is None:
        return {"message": "Movie not found"}
    return [model_to_dict(actor) for actor in movie.actors]

@app_movies_orm.post("/movies")
def add_orm_movie(params: dict[str, Any]):
    movie = Movie.create(**params)
    return {"message": f"Movie added successfully. ID: {movie.id}", "movie_id": movie.id}

@app_movies_orm.delete("/movies/{movie_id}")
def delete_orm_movie(movie_id: int):
    query = Movie.delete().where(Movie.id == movie_id)
    count = query.execute()
    if count == 0:
        return {"message": f"no movie found by id: {movie_id}"}
    return {"message": f"Movie with ID {movie_id} deleted successfully."}

@app_movies_orm.delete("/movies")
def delete_orm_movies(ids: list[int]):
    query = Movie.delete().where(Movie.id << ids)
    count = query.execute()
    return {"message": f"Deleted {count} movies."}

@app_movies_orm.put("/movies/{movie_id}")
def update_orm_movie(movie_id: int, params: dict[str, Any]):
    query = Movie.update(**params).where(Movie.id == movie_id)
    updated = query.execute()
    if not updated:
        return {"message": "Movie not found"}
    return {"message": f"Movie with ID {movie_id} updated successfully."}

@app_movies_orm.get("/actors")
async def get_orm_actors():
    actors_list = list(Actor.select().dicts())
    return actors_list

@app_movies_orm.get("/actors/{actor_id}")
async def get_orm_single_actor(actor_id:int):
    actor = Actor.get_or_none(Actor.id == actor_id)
    if actor is None:
        return {"message": "Actor not found"}
    return model_to_dict(actor)

@app_movies_orm.post("/actors")
async def add_orm_actor(params: dict[str, Any]):
    actor = Actor.create(**params)
    return {"message": f"Actor added successfully. ID: {actor.id}", "actor_id": actor.id}

@app_movies_orm.put("/actors/{id}")
async def update_orm_actor(id: int, params: dict[str, Any]):
    actor = Actor.get_or_none(Actor.id == id)
    if actor is None:
        return {"message": "Actor not found"}
    for key, value in params.items():
        setattr(actor, key, value)
    actor.save()
    return model_to_dict(actor)

@app_movies_orm.delete("/actors/{id}")
async def delete_orm_actor(id: int):
    actor = Actor.get_or_none(Actor.id == id)
    if actor is None:
        return {"message": "Actor not found"}
    # TODO: block deletion if actor is still in use
    actor.delete_instance()
    return {"message": f"Actor with ID {id} deleted successfully."}
