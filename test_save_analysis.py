import os
import tempfile
import unittest
from unittest.mock import patch

from flask import Flask
from sqlalchemy.exc import SQLAlchemyError

from app import Analysis, app, db, save_analysis


class TestSaveAnalysis(unittest.TestCase):
    def setUp(self):
        # Use a separate database so tests do not change saved coursework.
        self.folder = tempfile.TemporaryDirectory()
        self.database_path = os.path.join(self.folder.name, "test.db")
        self.test_app = Flask(__name__)
        self.test_app.config["SQLALCHEMY_DATABASE_URI"] = (
            "sqlite:///" + self.database_path
        )
        self.test_app.config["TESTING"] = True
        db.init_app(self.test_app)
        self.test_app.add_url_rule(
            "/save_analysis", view_func=save_analysis, methods=["POST"]
        )
        with self.test_app.app_context():
            db.create_all()
        self.client = self.test_app.test_client()
        self.data = {"algorithm": "stack_reverse", "step": 10, "n_max": 100}

    def tearDown(self):
        with self.test_app.app_context():
            db.session.remove()
            db.engine.dispose()
        self.folder.cleanup()

    def test_endpoint_registered_in_main_app(self):
        response = app.test_client().post("/save_analysis", json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(app.test_client().get("/save_analysis").status_code, 405)

    def test_save_persists_in_database(self):
        response = self.client.post("/save_analysis", json=self.data)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data["algorithm"], "stack_reverse")
        self.assertEqual(data["step"], 10)
        self.assertEqual(data["n_max"], 100)

        # Close the connection, then read the saved row with a new connection.
        with self.test_app.app_context():
            db.session.remove()
            db.engine.dispose()
            saved = db.session.get(Analysis, data["id"])
            self.assertEqual(saved.algorithm, "stack_reverse")
            self.assertEqual(saved.step, 10)
            self.assertEqual(saved.n_max, 100)
        self.assertTrue(os.path.isfile(self.database_path))

    def test_multiple_saves_and_zero_max(self):
        first = self.client.post("/save_analysis", json=self.data)
        self.data["n_max"] = 0
        second = self.client.post("/save_analysis", json=self.data)
        self.assertEqual(first.status_code, 201)
        self.assertEqual(second.status_code, 201)
        self.assertNotEqual(first.get_json()["id"], second.get_json()["id"])
        with self.test_app.app_context():
            rows = db.session.execute(db.select(Analysis)).scalars().all()
            self.assertEqual(len(rows), 2)
            saved = db.session.get(Analysis, second.get_json()["id"])
            self.assertEqual(saved.n_max, 0)

    def test_invalid_fields_do_not_save(self):
        invalid_values = {
            "algorithm": [None, "unknown", [], {}],
            "step": [None, 0, -1, 1.5, "10", True],
            "n_max": [None, -1, 1.5, "100", False],
        }
        for field, values in invalid_values.items():
            for value in values:
                with self.subTest(field=field, value=value):
                    data = self.data.copy()
                    data[field] = value
                    response = self.client.post("/save_analysis", json=data)
                    self.assertEqual(response.status_code, 400)
            data = self.data.copy()
            del data[field]
            self.assertEqual(
                self.client.post("/save_analysis", json=data).status_code, 400
            )
        with self.test_app.app_context():
            rows = db.session.execute(db.select(Analysis)).scalars().all()
            self.assertEqual(rows, [])

    def test_invalid_request_body(self):
        for body in ["", "{", "null", "[]", '"hello"']:
            with self.subTest(body=body):
                response = self.client.post(
                    "/save_analysis", data=body, content_type="application/json"
                )
                self.assertEqual(response.status_code, 400)
        response = self.client.post("/save_analysis", data=self.data)
        self.assertEqual(response.status_code, 400)

    def test_database_failure_and_next_save(self):
        with patch.object(db.session, "commit", side_effect=SQLAlchemyError):
            response = self.client.post("/save_analysis", json=self.data)
            self.assertEqual(response.status_code, 500)
        response = self.client.post("/save_analysis", json=self.data)
        self.assertEqual(response.status_code, 201)
        with self.test_app.app_context():
            rows = db.session.execute(db.select(Analysis)).scalars().all()
            self.assertEqual(len(rows), 1)


if __name__ == "__main__":
    unittest.main()
