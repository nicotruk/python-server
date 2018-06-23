# Lo siguiente debe inicializarse en setup.py
import os
import sys

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
########
import unittest
from config.mongodb import db
from app import app
from mock import patch
import json
import config.firebase_config

test_user = {
    "username": "asd",
    "password": "123",
    "email": "asd@asd.com",
    "name": "Nombre Apellido",
    "profile_pic": "",
    "firebase_token": "fdsfsdfjsdkfhsdjklhjk23h4234"
}

test_story = {
    "location": "",
    "visibility": "public",
    "title": "un titulo",
    "description": "una descripcion",
    "is_quick_story": "true",
    "timestamp": "1529448160000"
}

headers = {'content-type': 'application/json', 'Authorization': 'Bearer {}'.format("asd")}


class StoriesResourceTestCase(unittest.TestCase):

    def setUp(self):
        config.firebase_config.FIREBASE_NOTIFICATIONS_ENABLED = False
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        with app.app_context():
            db.stories.delete_many({})
            db.users.delete_many({})

    @patch('requests.post')
    def test_get_all_stories_nonexistent_user(self, mock_post):
        mock_post.return_value.status_code = 200
        response = self.app.get("/api/v1/stories?user_id=sarasa", headers=headers)
        self.assertEqual(response.status_code, 403)

    @patch('resources.user_resource.requests.post')
    def test_get_all_stories_empty(self, mock_post):
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
        response = self.app.get("/api/v1/stories?user_id={}".format(user_id), headers=headers)
        self.assertEqual(response.status_code, 200)
        stories_response = json.loads(response.data)
        stories = stories_response["stories"]
        self.assertEqual(len(stories), 0)

    @patch('resources.user_resource.requests.post')
    def test_post_story(self, mock_post):
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
        response = self.app.post("/api/v1/stories",
                                 data=json.dumps(story),
                                 headers=headers)
        self.assertEqual(response.status_code, 200)
        response = self.app.get("/api/v1/stories?user_id={}".format(user_id), headers=headers)
        stories_response = json.loads(response.data)
        stories = stories_response["stories"]
        self.assertEqual(len(stories), 1)
        self.assertEqual(stories[0]["title"], test_story["title"])
        self.assertEqual(stories[0]["description"], test_story["description"])

    @patch('resources.user_resource.requests.post')
    def test_post_and_delete_story(self, mock_post):
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
        response = self.app.post("/api/v1/stories",
                                 data=json.dumps(story),
                                 headers=headers)
        response_story = json.loads(response.data)

        response = self.app.delete("/api/v1/stories/{}".format(response_story["id"]), headers=headers)
        self.assertEqual(response.status_code, 201)

    @patch('requests.post')
    def test_delete_nonexistent_story(self, mock_post):
        mock_post.return_value.status_code = 200
        response = self.app.delete("/api/v1/stories/{}".format("sarasa"), headers=headers)
        self.assertEqual(response.status_code, 403)
