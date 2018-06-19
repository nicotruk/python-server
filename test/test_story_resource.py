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

test_user = {
    "username": "asd",
    "password": "123",
    "email": "asd@asd.com",
    "name": "Nombre Apellido",
    "profile_pic": "",
    "firebase_token": "fdsfsdfjsdkfhsdjklhjk23h4234",
}


class StoriesResourceTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        with app.app_context():
            db.stories.delete_many({})
            db.users.delete_many({})

    def test_get_all_stories_nonexistent_user(self):
        response = self.app.get("/api/v1/stories?user_id=sarasa")
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
        response = self.app.get("/api/v1/stories?user_id={}".format(user_id))
        self.assertEqual(response.status_code, 200)
        stories_response = json.loads(response.data)
        stories = stories_response["stories"]
        self.assertEqual(len(stories), 0)
