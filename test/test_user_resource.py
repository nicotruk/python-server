# Lo siguiente debe inicializarse en setup.py
import os
import sys

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
########
from config.mongodb import db
from app import app
from mock import patch
import unittest
import json

test_user = {
    "username": "asd",
    "password": "123",
    "email": "asd@asd.com",
    "first_name": "Nombre",
    "last_name": "Apellido" 
}


class UsersResourceTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        with app.app_context():
            db.users.delete_many({})

    def test_get_all_users(self):
        response = self.app.get("/api/v1/users")
        self.assertEqual(response.status_code, 200)

    @patch('resources.user_resource.requests.post')
    def test_post_user(self, mock_post):
        mock_post.return_value.status_code = 200

        user = test_user.copy()

        response = self.app.post("/api/v1/users",
                                 data=json.dumps(user),
                                 content_type='application/json')

        user_response = json.loads(response.data)
        user.pop('password')
        user["user_id"] = user_response["user"]["user_id"]
        self.assertEqual(user, user_response["user"])

    @patch('resources.user_resource.requests.post')
    def test_update_user(self, mock_post):
        mock_post.return_value.status_code = 200

        user = test_user.copy()

        post_response = self.app.post("/api/v1/users",
                                 data=json.dumps(user),
                                 content_type='application/json')

        user_response = json.loads(post_response.data)
        user_id = user_response["user"]["user_id"]

        changes = {
            "first_name": "new_name",
            "last_name": "new_last_name",
            "email": "new_email",
            "profile_pic": "new_profile_pic"
        }

        update_response = self.app.put("/api/v1/users/{}".format(user_id),
                                 data=json.dumps(changes),
                                 content_type='application/json')

        json_response = json.loads(update_response.data)

        self.assertEqual(json_response["user"]["first_name"], changes["first_name"])
        self.assertEqual(json_response["user"]["last_name"], changes["last_name"])
        self.assertEqual(json_response["user"]["email"], changes["email"])
        self.assertEqual(json_response["user"]["profile_pic"], changes["profile_pic"])

    def test_get_single_user_error_user_not_found(self):
        response = self.app.get("/api/v1/users/1234")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(json.loads(response.data)["message"], "There is no user with that ID!")

    @patch('resources.user_resource.requests.post')
    def test_login(self, mock_post):
        user = test_user.copy()

        post_response = self.app.post("/api/v1/users",
                                 data=json.dumps(user),
                                 content_type='application/json')

        response = {
            "token": {
                "expiresAt": "123",
                "token": "asd"
            }
        }
        mock_post.return_value.text = json.dumps(response)
        mock_post.return_value.status_code = 200

        user = {
            "username": "asd",
            "password": "123"
        }
        response = self.app.post("/api/v1/users/login",
                                 data=json.dumps(user),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 200)

    @patch('resources.user_resource.requests.post')
    def test_integration_create_user(self, mock_post):
        mock_post.return_value.status_code = 200

        user = test_user.copy()
        user["profile_pic"] = ''
        user["friends_ids"] = []

        response = self.app.post("/api/v1/users",
                                 data=json.dumps(user),
                                 content_type='application/json')

        user_response = json.loads(response.data)
        user.pop('password')
        user["user_id"] = user_response["user"]["user_id"]

        getResponse = self.app.get("/api/v1/users")
        self.assertIn(user, json.loads(getResponse.data)["users"])

    @patch('resources.user_resource.requests.post')
    def test_integration_get_single_user(self, mock_post):
        mock_post.return_value.status_code = 200

        user = test_user.copy()
        user["profile_pic"] = ''
        user["friends_ids"] = []

        response = self.app.post("/api/v1/users",
                                 data=json.dumps(user),
                                 content_type='application/json')

        user_response = json.loads(response.data)
        user.pop('password')
        user["user_id"] = user_response["user"]["user_id"]

        get_response = self.app.get('/api/v1/users/{}'.format(user["user_id"]))
        self.assertEqual(user, json.loads(get_response.data)["user"])
