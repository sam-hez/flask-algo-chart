import base64
import os
import tempfile
import unittest

import app


class TestVisualizer(unittest.TestCase):
    def setUp(self):
        self.client = app.app.test_client()
        self.folder = tempfile.TemporaryDirectory()
        self.old_folder = app.IMAGE_FOLDER
        app.IMAGE_FOLDER = self.folder.name

    def tearDown(self):
        app.IMAGE_FOLDER = self.old_folder
        self.folder.cleanup()

    def test_home(self):
        self.assertEqual(self.client.get("/").status_code, 200)

    def test_operation_counts(self):
        expected = {"linear_search": 4, "bubble_sort": 16,
                    "binary_search": 2, "nested_loops": 16,
                    "stack_reverse": 8, "stack_search": 12,
                    "queue_process": 14}
        for algo in expected:
            with self.subTest(algo=algo):
                self.assertEqual(app.calculate_operations(algo, 4), expected[algo])
                self.assertEqual(app.calculate_operations(algo, 0), 0)

    def test_all_algorithms_generate_png(self):
        for algo in app.SUPPORTED_ALGORITHMS:
            with self.subTest(algo=algo):
                response = self.client.get("/analyze", query_string={
                    "algo": algo, "step": 3, "n_max": 10})
                self.assertEqual(response.status_code, 200)
                data = response.get_json()
                self.assertEqual(data["algorithm"], algo)
                image = base64.b64decode(data["image_base64"])
                self.assertTrue(image.startswith(b"\x89PNG\r\n\x1a\n"))
                with open(data["image_path"], "rb") as saved:
                    self.assertEqual(saved.read(), image)

    def test_zero_and_step_larger_than_max(self):
        for n_max in [0, 2]:
            response = self.client.get("/analyze", query_string={
                "algo": "stack_reverse", "step": 10, "n_max": n_max})
            self.assertEqual(response.status_code, 200)
            self.assertTrue(os.path.exists(response.get_json()["image_path"]))

    def test_comma_in_number(self):
        response = self.client.get(
            "/analyze?algo=stack_reverse&step=1,000&n_max=1,000")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["n_max"], 1000)

    def test_invalid_requests(self):
        queries = ["", "algo=unknown&step=1&n_max=10",
                   "algo=stack_reverse&n_max=10",
                   "algo=stack_reverse&step=1",
                   "algo=stack_reverse&step=0&n_max=10",
                   "algo=stack_reverse&step=-1&n_max=10",
                   "algo=stack_reverse&step=abc&n_max=10",
                   "algo=stack_reverse&step=1.5&n_max=10",
                   "algo=queue_process&step=1&n_max=-1",
                   "algo=queue_process&step=1&n_max=abc"]
        for query in queries:
            with self.subTest(query=query):
                response = self.client.get("/analyze?" + query)
                self.assertEqual(response.status_code, 400)
                self.assertIn("error", response.get_json())


if __name__ == "__main__":
    unittest.main()
