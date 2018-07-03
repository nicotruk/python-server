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

time_val = round(time.time())

test_user = {
    "username": "asd",
    "password": "123",
    "email": "asd@asd.com",
    "name": "Nombre Apellido",
    "profile_pic": "",
    "firebase_token": "fdsfsdfjsdkfhsdjklhjk23h4234",
}

test_story = {
    "location": "",
    "visibility": "public",
    "title": "un titulo",
    "description": "una descripcion",
    "is_quick_story": "true",
    "timestamp": "1529448160"
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
            db.stories.delete_many({})
            db.requests_stats.delete_many({})

    @patch('resources.token_validation_decorator.requests.post')
    def test_get_stats(self, mock_post):
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
    def test_get_stats_last_60_min(self, mock_post, mock_time):
        mock_time.return_value = time_val
        mock_post.return_value.status_code = 200
        self.app.get("/api/v1/users", headers=headers)
        response = self.app.get("/api/v1/stats/last/60")
        self.assertEqual(response.status_code, 200)
        stats = json.loads(response.data)["stats"]
        self.assertEqual(len(stats), 1)
        mock_time.return_value = time_val + 65 * 60 * 1000
        response = self.app.get("/api/v1/stats/last/60")
        self.assertEqual(response.status_code, 200)
        stats = json.loads(response.data)["stats"]
        self.assertEqual(len(stats), 0)

    @patch('resources.token_validation_decorator.requests.post')
    def test_get_stats_last_aa_min(self, mock_post):
        mock_post.return_value.status_code = 200
        self.app.get("/api/v1/users", headers=headers)
        response = self.app.get("/api/v1/stats/last/aa")
        self.assertEqual(response.status_code, 500)

    @patch('time.time')
    @patch('requests.post')
    @patch('requests.get')
    def test_get_stories_stats(self, mock_get, mock_post, mock_time):
        mock_time.return_value = time_val
        mock_get.return_value.status_code = 200
        mock_post.return_value.status_code = 200
        response = {
            "token": {
                "expiresAt": "123",
                "token": "asd"
            }
        }
        mock_post.return_value.text = json.dumps(response)
        user = test_user.copy()
        response = self.app.post("/api/v1/users",
                                 data=json.dumps(user),
                                 content_type='application/json')
        user_response = json.loads(response.data)
        user_id = user_response["user"]["user_id"]

        story = test_story.copy()
        story["user_id"] = user_id
        self.app.post("/api/v1/stories",
                      data=json.dumps(story),
                      headers=headers)
        response = self.app.get("/api/v1/stats")
        self.assertEqual(response.status_code, 200)
        stats = json.loads(response.data)["stats"]
        self.assertEqual(len(stats), 2)
        response = self.app.get("/api/v1/stats/stories")
        self.assertEqual(response.status_code, 200)
        stats = json.loads(response.data)["stats"]
        self.assertEqual(len(stats), 1)
        self.assertIn("/api/v1/stories", stats[0]["request"])
        mock_time.return_value = time_val + 10 * 24 * 60 * 60 * 1000
        response = self.app.get("/api/v1/stats/stories")
        self.assertEqual(response.status_code, 200)
        stats = json.loads(response.data)["stats"]
        self.assertEqual(len(stats), 0)
