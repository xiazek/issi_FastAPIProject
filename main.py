import os

import requests

from ensure_movies_db_exists import ensure_movies_db_exists
from app_movies_orm import app_movies_orm
from app_movies_pure_sql import app_movies_pure_sql


app = app_movies_pure_sql
debug = os.getenv("DEBUG") == "1"
app.debug = debug
ensure_movies_db_exists("movies-extended.db")
ensure_movies_db_exists("movies.db")


# UWAGA. Endpointy związane z filmami są zdefiniowane w osobnych plikach:
# - app_movies_pure_sql.py
# - app_movies_orm.py
# szczegóły w README.md


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/sum")
async def calculate_sum(x: int = 0, y: int = 10):
    return x + y

@app.get("/subtract")
async def calculate_subtraction(x: int = 10, y: int = 0):
    return x - y

@app.get("/multiply")
async def calculate_multiplication(x: int = 10, y: int = 10):
    return x * y

@app.get("/divide")
async def calculate_division(x: int = 10, y: int = 2):
    if y == 0:
        return {"error": "Cannot divide by zero"}

    return x / y


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


app.mount("/orm", app_movies_orm)
# UWAGA! Endpointy związane z filmami są zdefiniowane w osobnych plikach:
# - app_movies_pure_sql.py
# - app_movies_orm.py
# szczegóły w README.md
