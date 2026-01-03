import unittest
import os
import shutil
from fastapi.testclient import TestClient
from app_movies_pure_sql import app_movies_pure_sql

class TestPureSQL(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.makedirs("tmp", exist_ok=True)
        cls.db_path = "tmp/movies_test_pure.db"
        if os.path.exists("movies.db.template"):
            shutil.copy2("movies.db.template", cls.db_path)
        os.environ["MOVIES_DB"] = cls.db_path
        cls.client = TestClient(app_movies_pure_sql)

    def test_get_movies(self):
        response = self.client.get("/movies")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_add_movie(self):
        movie_data = {"title": "Test Movie", "year": 2023, "actors": "Test Actor"}
        response = self.client.post("/movies", json=movie_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Movie added successfully", response.json()["message"])
        movie_id = response.json()["movie_id"]

        # Verify it was added
        response = self.client.get(f"/movies/{movie_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Test Movie")

    def test_update_movie(self):
        # First add a movie
        movie_data = {"title": "Update Me", "year": 2020, "actors": "Some Actor"}
        add_res = self.client.post("/movies", json=movie_data)
        movie_id = add_res.json()["movie_id"]

        # Update it
        update_data = {"title": "Updated Title", "year": 2021, "actors": "Updated Actor"}
        response = self.client.put(f"/movies/{movie_id}", json=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("updated successfully", response.json()["message"])

        # Verify update
        response = self.client.get(f"/movies/{movie_id}")
        self.assertEqual(response.json()["title"], "Updated Title")

    def test_delete_movie(self):
        # First add a movie
        movie_data = {"title": "Delete Me", "year": 2000, "actors": "Actor"}
        add_res = self.client.post("/movies", json=movie_data)
        movie_id = add_res.json()["movie_id"]

        # Delete it
        response = self.client.delete(f"/movies/{movie_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("deleted successfully", response.json()["message"])

        # Verify it's gone
        response = self.client.get(f"/movies/{movie_id}")
        self.assertEqual(response.json()["message"], "Movie not found")

if __name__ == "__main__":
    unittest.main()
