# Lo siguiente debe inicializarse en setup.py
import os
import sys

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
########
from config.mongodb import db
from app import app
import unittest
import config.firebase_config
from mock import patch
import json
import time
from datetime import datetime

time_val = round(time.time())

test_user = {
    "username": "asd",
    "password": "123",
    "email": "asd@asd.com",
    "name": "Nombre Apellido",
    "profile_pic": "",
    "firebase_token": "fdsfsdfjsdkfhsdjklhjk23h4234",
}

headers = {'content-type': 'application/json', 'Authorization': 'Bearer {}'.format("asd")}


class StatsResourceTestCase(unittest.TestCase):

    def setUp(self):
        config.firebase_config.FIREBASE_NOTIFICATIONS_ENABLED = False
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        with app.app_context():
            db.users.delete_many({})
            db.requests_stats.delete_many({})

    @patch('resources.token_validation_decorator.requests.post')
    def test_get_all_users(self, mock_post):
        response = self.app.get("/api/v1/stats")
        self.assertEqual(response.status_code, 200)
        stats = json.loads(response.data)["stats"]
        self.assertEqual(len(stats), 0)
        mock_post.return_value.status_code = 200
        self.app.get("/api/v1/users", headers=headers)
        response = self.app.get("/api/v1/stats")
        self.assertEqual(response.status_code, 200)
        stats = json.loads(response.data)["stats"]
        self.assertEqual(len(stats), 1)
        self.assertIn("/api/v1/users", stats[0]["request"])

    @patch('time.time')
    @patch('resources.token_validation_decorator.requests.post')
    def test_get_all_users(self, mock_post, mock_time):
        mock_time.return_value = time_val
        mock_post.return_value.status_code = 200
        self.app.get("/api/v1/users", headers=headers)
        response = self.app.get("/api/v1/stats/last/60")
        self.assertEqual(response.status_code, 200)
        stats = json.loads(response.data)["stats"]
        self.assertEqual(len(stats), 1)
        mock_time.return_value = time_val + 65*60*1000
        response = self.app.get("/api/v1/stats/last/60")
        self.assertEqual(response.status_code, 200)
        stats = json.loads(response.data)["stats"]
        self.assertEqual(len(stats), 0)
