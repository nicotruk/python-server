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


class FileResourceTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        with app.app_context():
            db.stories.delete_many({})
            db.users.delete_many({})

    @patch('requests.post')
    def test_post_file(self, mock_post):
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
                                 content_type='application/json')
        response_story = json.loads(response.data)

        story_id = response_story["id"]

        mock_post.return_value.status_code = 200
        file_url = "urlDelFile"
        mock_story_response = {
            "file": {
                "resource": file_url
            }
        }
        mock_post.return_value.text = json.dumps(mock_story_response)

        data = dict(
            file=(open(myPath + '/files/android.png', 'rb'), "android.png"),
        )
        response = self.app.post("/api/v1/stories/{}/files".format(story_id),
                                 data=data,
                                 content_type='multipart/form-data')
        updated_story = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(file_url, updated_story["file_url"])
