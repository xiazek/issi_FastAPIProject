import sqlite3
from dataclasses import dataclass


@dataclass
class MoviesStorage:
    """
    Handles storage and retrieval of movie data using a PURE SQL approach.
    See oem_models.py for an ORM version.
    """
    _db: sqlite3.Connection
    _cursor: sqlite3.Cursor

    @classmethod
    def default(cls):
        db = sqlite3.connect('movies.db')
        db.row_factory = sqlite3.Row  # <-- enables dict-like access
        return cls(_db=db, _cursor=db.cursor())

    def list(self):
        self._cursor.execute('SELECT * FROM movies')
        return self._cursor.fetchall()

    def find_by_id(self, movie_id: int):
        self._cursor.execute('SELECT * FROM movies WHERE ID = ?', (movie_id,))
        return self._cursor.fetchone()

    def search(self, query: str):
        self._cursor.execute(
            'SELECT * FROM movies WHERE title like ? OR actors LIKE ?',
            (f"%{query}%", f"%{query}%")
        )
        return self._cursor.fetchall()

    def add_movie(self, form: dict):
        """
        Adds a new movie to the storage.

        :param form: A dictionary containing 'title', 'year', and 'actors'.
        :return: The ID of the newly inserted movie.
        """
        self._cursor.execute(
            "INSERT INTO movies (title, year, actors) VALUES (:title, :year, :actors)",
            {"title": form['title'], "year": form['year'], "actors": form['actors']},
        )
        self._db.commit()
        return self._cursor.lastrowid

    def delete_movies_by_id(self, ids: list):
        placeholders = ', '.join(['?'] * len(ids))
        self._cursor.execute(f"DELETE FROM movies WHERE id IN ({placeholders})", ids)
        self._db.commit()
        return self._cursor.rowcount

    def update_movie(self, movie_id: int, form: dict):
        """
        Updates an existing movie.

        :param movie_id: The ID of the movie to update.
        :param form: A dictionary containing 'title', 'year', and 'actors'.
        :return: True if the movie was updated, False otherwise.
        """
        self._cursor.execute(
            "UPDATE movies SET title = :title, year = :year, actors = :actors WHERE id = :id",
            {"title": form['title'], "year": form['year'], "actors": form['actors'], "id": movie_id},
        )
        self._db.commit()
        return self._cursor.rowcount > 0
