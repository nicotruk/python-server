import os
import sys
import uuid

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
########
from config.mongodb import db
from app import app
import unittest
import json
import config.firebase_config

test_user = {
    "username": "",
    "password": "123",
    "email": "asd@asd.com",
    "name": "Nombre Apellido",
    "profile_pic": "",
    "firebase_token": "fdsfsdfjsdkfhsdjklhjk23h4234",
}

test_story = {
    "user_id": "",
    "location": "",
    "visibility": "public",
    "title": "un titulo",
    "description": "una descripcion",
    "is_quick_story": "true",
    "timestamp": "2018-06-25 15:44:05"
}


class IntegrationTests(unittest.TestCase):

    def setUp(self):
        config.firebase_config.FIREBASE_NOTIFICATIONS_ENABLED = False
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        with app.app_context():
            db.users.delete_many({})
            db.friendship_requests.delete_many({})
            db.requests_stats.delete_many({})
            db.stories.delete_many({})

    def test_post_user_and_post_story_success(self):
        user = test_user.copy()
        user["username"] = str(uuid.uuid4())

        user_response = self.app.post("/api/v1/users",
                                 data=json.dumps(user))

        user_response_data = json.loads(user_response.data)
        self.assertEqual(user_response.status_code, 201)

        story = test_story.copy()
        story["user_id"] = user_response_data["user"]["user_id"]
        user_token = user_response_data["token"]["token"]
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer {}'.format(user_token)}

        story_response = self.app.post("/api/v1/stories",
                                 data=json.dumps(story),
                                 headers=headers)

        self.assertEqual(story_response.status_code, 200)

    def test_post_user_error(self):
        repeated_username = str(uuid.uuid4())

        user = test_user.copy()
        user["username"] = repeated_username

        user_response_1 = self.app.post("/api/v1/users",
                                 data=json.dumps(user))

        self.assertEqual(user_response_1.status_code, 201)

        user_response_2 = self.app.post("/api/v1/users",
                                        data=json.dumps(user))

        self.assertEqual(user_response_2.status_code, 409)

    def test_post_story_unauthorized(self):
        user = test_user.copy()
        user["username"] = str(uuid.uuid4())

        user_response = self.app.post("/api/v1/users",
                                      data=json.dumps(user))

        user_response_data = json.loads(user_response.data)
        self.assertEqual(user_response.status_code, 201)

        story = test_story.copy()
        story["user_id"] = user_response_data["user"]["user_id"]
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer wrong_token'}

        story_response = self.app.post("/api/v1/stories",
                                       data=json.dumps(story),
                                       headers=headers)

        self.assertEqual(story_response.status_code, 401)