import unittest
import logging
from app import app

logger = logging.getLogger(__name__)

class TestMovements(unittest.TestCase):

    def test_valid_date(self):
        with app.test_client() as client:
            response = client.post('/movements?date=27/01/2023')
            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(response.json, list)

    def test_missing_date_parameter(self):
        with app.test_client() as client:
            response = client.post('/movements')
            self.assertEqual(response.status_code, 400)

    def test_invalid_date_parameter(self):
        with app.test_client() as client:
            response = client.post('/movements?date=2023-02-22')
            self.assertEqual(response.status_code, 400)

    def test_no_data_for_date(self):
        with app.test_client() as client:
            response = client.post('/movements?date=01/01/2023')
            self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()