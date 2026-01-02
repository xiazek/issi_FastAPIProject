# ORM version
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

