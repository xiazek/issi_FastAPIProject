# Zadanie na zaliczenie przedmiotu "Wybrane zagadnienia z inżynierii oprogramowania"
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

Do testowania punktów końcowych API można użyć pliku `test_main.http`. Jest to format obsługiwany przez IDE takie jak PyCharm czy VS Code (z odpowiednim rozszerzeniem), który umożliwia bezpośrednie wysyłanie żądań HTTP do uruchomionej aplikacji.

## Funkcjonalności
- [Przeglądanie listy filmów](http://127.0.0.1:8000/movies)
- [Pobieranie szczegółów filmu](http://127.0.0.1:8000/movies/1)
- Dodawanie nowych filmów
- Usuwanie filmów (pojedynczo lub masowo)
- Aktualizacja danych o filmach
- [Reverse-geokoding na podstawie współrzędnych](http://127.0.0.1:8000/geocode?lat=50.0680275&lon=19.9098668)

Pozostałe funkcjonalności (dodawanie, usuwanie, edycja) można przetestować za pomocą pliku [test_main.http](test_main.http).
