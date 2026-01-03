import unittest
import os
import shutil
from fastapi.testclient import TestClient
from orm_models import db

class TestORM(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.makedirs("tmp", exist_ok=True)
        cls.db_path = "tmp/movies_test_orm.db"
        if os.path.exists("movies-extended.db.template"):
            shutil.copy2("movies-extended.db.template", cls.db_path)
        os.environ["MOVIES_EXTENDED_DB"] = cls.db_path

        # We need to re-initialize the database connection in orm_models
        # because it might have already connected to the default path
        # during import.
        db.init(cls.db_path)

        # pylint: disable=import-outside-toplevel
        from app_movies_orm import app_movies_orm
        cls.client = TestClient(app_movies_orm)

    def test_get_movies(self):
        response = self.client.get("/movies")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_add_movie(self):
        movie_data = {
            "title": "ORM Movie", 
            "director": "Director", 
            "year": 2023, 
            "description": "Desc"
        }
        response = self.client.post("/movies", json=movie_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Movie added successfully", response.json()["message"])
        movie_id = response.json()["movie_id"]

        # Verify it was added
        response = self.client.get(f"/movies/{movie_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "ORM Movie")

    def test_get_actors(self):
        response = self.client.get("/actors")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

if __name__ == "__main__":
    unittest.main()
