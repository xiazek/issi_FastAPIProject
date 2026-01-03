# Zadanie na zaliczenie przedmiotu "Wybrane zagadnienia z inżynierii oprogramowania"

[![lint and test](https://github.com/xiazek/issi_FastAPIProject/actions/workflows/lint_and_test.yml/badge.svg)](https://github.com/xiazek/issi_FastAPIProject/actions/workflows/lint_and_test.yml)

## Opis projektu

API do zarządzania filmami, zbudowane przy użyciu FastAPI.

## Wymagania
- Python >= 3.13
- uv (menedżer pakietów dla Pythona)
- Pełna lista zależności znajduje się w pliku [pyproject.toml](pyproject.toml)

## Instalacja

1. Sklonuj repozytorium:
```bash
git clone <url-repozytorium>
cd FastAPIProject
```

2. Zainstaluj zależności przy użyciu `uv`:
```bash
uv sync
```

## Baza danych

Przy każdym uruchomieniu aplikacji sprawdzane jest, czy plik bazy danych `movies.db` istnieje. Jeśli nie, zostaje on automatycznie utworzony na podstawie pliku szablonu `movies.db.template`.
To samo dotyczy bazy danych `movies-extended.db` i szablonu `movies-extended.db.template`.

## Uruchamianie aplikacji

Uruchom aplikację FastAPI:
```bash
uv run fastapi dev main.py
```
Aplikacja będzie dostępna pod adresem: `http://127.0.0.1:8000`
Dokumentacja Swagger UI dostępna pod adresem: `http://127.0.0.1:8000/docs`

## Analiza kodu

Do sprawdzania jakości kodu używany jest `pylint`. Możesz go uruchomić za pomocą `uv`:
```bash
uv run pylint .
```
Konfiguracja `pylint` znajduje się w pliku [pyproject.toml](pyproject.toml).

## Testowanie

Do testowania endpointów API można użyć pliku `test_main.http`. Jest to format obsługiwany przez IDE takie jak PyCharm czy VS Code (z odpowiednim rozszerzeniem), który umożliwia bezpośrednie wysyłanie żądań HTTP do uruchomionej aplikacji.

## Funkcjonalności

Endpointy API są podzielone na trzy grupy.
Uwaga: aplikacja udostępnia dwie wersje obsługi filmów:
- Wersję opartą na czystym SQL (obsługuje prostą wersję movies.db przy pomocy [klasy MoviesStorage](movies_storage.py))
- Oraz wersję korzystającą z Peewee ORM.

### 1. Ogólne endpointy (zdefiniowane w `main.py`)

- `GET /` - Powitanie (Hello World)
- `GET /hello/{name}` - Powitanie z imieniem
- `GET /sum` - Obliczanie sumy dwóch liczb (`x`, `y`)
- `GET /geocode` - Reverse-geocoding na podstawie współrzędnych (`lat`, `lon`)

### 2. Movies: wersja Pure SQL (dostępna pod prefiksem `/`)

Te endpointy używają `app_movies_pure_sql.py` i operują na bazie `movies.db`.

- `GET /movies` - [Przeglądanie listy filmów](http://127.0.0.1:8000/movies)
- `GET /movies/{movie_id}` - [Pobieranie szczegółów filmu](http://127.0.0.1:8000/movies/1)
- `POST /movies` - Dodawanie nowych filmów
- `PUT /movies/{movie_id}` - Aktualizacja danych o filmie
- `DELETE /movies/{movie_id}` - Usuwanie pojedynczego filmu
- `DELETE /movies` - Masowe usuwanie filmów (lista ID w treści żądania)

### 3. Movies: wersja ORM (dostępna pod prefiksem `/orm`)

Te endpointy używają `app_movies_orm.py`, modeli Peewee z `orm_models.py` i operują na bazie `movies-extended.db`.

- `GET /orm/movies` - [Przeglądanie listy filmów (ORM)](http://127.0.0.1:8000/orm/movies)
- `GET /orm/movies/{movie_id}` - [Pobieranie szczegółów filmu (ORM)](http://127.0.0.1:8000/orm/movies/1)
- `POST /orm/movies` - Dodawanie nowych filmów (ORM)
- `PUT /orm/movies/{movie_id}` - Aktualizacja danych o filmie (ORM)
- `DELETE /orm/movies/{movie_id}` - Usuwanie pojedynczego filmu (ORM)
- `DELETE /orm/movies` - Masowe usuwanie filmów (ORM)
- `GET /orm/actors` - [Przeglądanie listy aktorów (ORM)](http://127.0.0.1:8000/orm/actors)
- `GET /orm/actors/{actor_id}` - [Pobieranie szczegółów aktora (ORM)](http://127.0.0.1:8000/orm/actors/1)

Pozostałe funkcjonalności (dodawanie, usuwanie, edycja) można przetestować za pomocą pliku [test_main.http](test_main.http) lub dokumentacji Swagger pod adresem `http://127.0.0.1:8000/docs`.
