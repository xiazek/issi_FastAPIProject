import unittest
import os
import shutil
from fastapi.testclient import TestClient
from orm_models import db

class TestMain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.makedirs("tmp", exist_ok=True)
        cls.db_path_pure = "tmp/movies_test_main_pure.db"
        cls.db_path_orm = "tmp/movies_test_main_orm.db"

        if os.path.exists("movies.db.template"):
            shutil.copy2("movies.db.template", cls.db_path_pure)
        if os.path.exists("movies-extended.db.template"):
            shutil.copy2("movies-extended.db.template", cls.db_path_orm)

        os.environ["MOVIES_DB"] = cls.db_path_pure
        os.environ["MOVIES_EXTENDED_DB"] = cls.db_path_orm

        db.init(cls.db_path_orm)

        # pylint: disable=import-outside-toplevel
        from main import app
        cls.client = TestClient(app)

    def test_root(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Hello World"})

    def test_pure_sql_integration(self):
        # Accessing pure sql routes through main app
        response = self.client.get("/movies")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_orm_integration(self):
        # Accessing orm routes through /orm mount
        response = self.client.get("/orm/movies")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_sum(self):
        response = self.client.get("/sum?x=5&y=10")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 15)

if __name__ == "__main__":
    unittest.main()
