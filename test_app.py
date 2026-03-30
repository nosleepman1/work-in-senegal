
import unittest
from unittest.mock import patch
from main import scrape_linkedin_jobs_senegal, MOCK_JOBS
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestJobsAPI(unittest.TestCase):

    def test_get_jobs_returns_list(self):
        response = client.get("/jobs?use_mock=true")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    @patch("main.requests.get")
    def test_scrape_falls_back_to_mock_on_error(self, mock_get):
        mock_get.side_effect = Exception("Connection error")
        result = scrape_linkedin_jobs_senegal()
        self.assertEqual(result, MOCK_JOBS)


if __name__ == "__main__":
    unittest.main()
