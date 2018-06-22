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
    "name": "Nombre Apellido",
    "profile_pic": "",
    "firebase_token": "fdsfsdfjsdkfhsdjklhjk23h4234",
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

        self.assertEqual(response.status_code, 200)
        user_response = json.loads(response.data)
        user.pop('password')
        user["user_id"] = user_response["user"]["user_id"]
        self.assertEqual(user, user_response["user"])

    def test_post_user_with_no_data(self):
        user = ""
        response = self.app.post("/api/v1/users",
                                 data=json.dumps(user),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 500)

    @patch('resources.user_resource.requests.post')
    def test_update_user(self, mock_post):
        mock_post.return_value.status_code = 200
        response = {
            "token": {
                "expiresAt": "123",
                "token": "asd"
            }
        }
        mock_post.return_value.text = json.dumps(response)

        user = test_user.copy()

        post_response = self.app.post("/api/v1/users",
                                      data=json.dumps(user),
                                      content_type='application/json')

        user_response = json.loads(post_response.data)
        user_id = user_response["user"]["user_id"]

        changes = {
            "name": "new_name",
            "email": "new_email",
            "profile_pic": "new_profile_pic"
        }

        update_response = self.app.put("/api/v1/users/{}".format(user_id),
                                       data=json.dumps(changes),
                                       content_type='application/json')

        json_response = json.loads(update_response.data)

        self.assertEqual(json_response["user"]["name"], changes["name"])
        self.assertEqual(json_response["user"]["email"], changes["email"])
        self.assertEqual(json_response["user"]["profile_pic"], changes["profile_pic"])

    @patch('resources.user_resource.requests.post')
    def test_update_firebase_token(self, mock_post):
        mock_post.return_value.status_code = 200
        response = {
            "token": {
                "expiresAt": "123",
                "token": "asd"
            }
        }
        mock_post.return_value.text = json.dumps(response)

        user = test_user.copy()

        post_response = self.app.post("/api/v1/users",
                                      data=json.dumps(user),
                                      content_type='application/json')

        user_response = json.loads(post_response.data)
        user_id = user_response["user"]["user_id"]

        changes = {
            "firebase_token": "newFirebaseToken"
        }

        update_response = self.app.put("/api/v1/users/firebase/{}".format(user_id),
                                       data=json.dumps(changes),
                                       content_type='application/json')

        json_response = json.loads(update_response.data)

        self.assertEqual(json_response["user"]["firebase_token"], changes["firebase_token"])

    def test_get_single_user_error_user_not_found(self):
        response = self.app.get("/api/v1/users/1234")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(json.loads(response.data)["message"], "There is no user with that ID!")

    @patch('resources.user_resource.requests.post')
    def test_login(self, mock_post):
        user = test_user.copy()

        self.app.post("/api/v1/users",
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
        response = {
            "token": {
                "expiresAt": "123",
                "token": "asd"
            }
        }
        mock_post.return_value.text = json.dumps(response)

        user = test_user.copy()
        user["profile_pic"] = ''
        user["friends_usernames"] = []

        response = self.app.post("/api/v1/users",
                                 data=json.dumps(user),
                                 content_type='application/json')

        user_response = json.loads(response.data)
        user.pop('password')
        user["user_id"] = user_response["user"]["user_id"]

        get_response = self.app.get("/api/v1/users")
        self.assertIn(user, json.loads(get_response.data)["users"])

    @patch('resources.user_resource.requests.post')
    def test_integration_get_single_user(self, mock_post):
        mock_post.return_value.status_code = 200
        response = {
            "token": {
                "expiresAt": "123",
                "token": "asd"
            }
        }
        mock_post.return_value.text = json.dumps(response)

        user = test_user.copy()
        user["profile_pic"] = ''
        user["friends_usernames"] = []

        response = self.app.post("/api/v1/users",
                                 data=json.dumps(user),
                                 content_type='application/json')

        user_response = json.loads(response.data)
        user.pop('password')
        user["user_id"] = user_response["user"]["user_id"]

        get_response = self.app.get('/api/v1/users/{}'.format(user["user_id"]))
        self.assertEqual(user, json.loads(get_response.data)["user"])

    @patch('resources.user_resource.requests.post')
    def test_user_search_no_match(self, mock_post):
        mock_post.return_value.status_code = 200
        response = {
            "token": {
                "expiresAt": "123",
                "token": "asd"
            }
        }
        mock_post.return_value.text = json.dumps(response)

        user = test_user.copy()
        friend_username = "amigacho"
        user["friends_usernames"] = [friend_username]
        response = self.app.post("/api/v1/users",
                                 data=json.dumps(user),
                                 content_type='application/json')
        user = json.loads(response.data)["user"]

        user2 = test_user.copy()
        user2["username"] = "anotherName"
        self.app.post("/api/v1/users",
                      data=json.dumps(user2),
                      content_type='application/json')

        query_username = user2["username"] + "1"
        self.assertGreater(len(query_username), len(user2["username"]))
        response = self.app.get("/api/v1/users/search/{}/{}".format(user["user_id"], query_username),
                     data=json.dumps(user),
                     content_type='application/json')
        found_users = json.loads(response.data)["found_users"]
        self.assertEqual(len(found_users), 0)

    @patch('resources.user_resource.requests.post')
    def test_user_search_one_match(self, mock_post):
        mock_post.return_value.status_code = 200
        response = {
            "token": {
                "expiresAt": "123",
                "token": "asd"
            }
        }
        mock_post.return_value.text = json.dumps(response)

        user = test_user.copy()
        friend_username = "amigacho"
        user["friends_usernames"] = [friend_username]
        response = self.app.post("/api/v1/users",
                                 data=json.dumps(user),
                                 content_type='application/json')
        user = json.loads(response.data)["user"]

        user2 = test_user.copy()
        user2["username"] = "anotherName"
        self.app.post("/api/v1/users",
                      data=json.dumps(user2),
                      content_type='application/json')
        user3 = test_user.copy()
        user3["username"] = "oneNoMatchingName"
        self.app.post("/api/v1/users",
                      data=json.dumps(user3),
                      content_type='application/json')

        query_username = user2["username"][0:-2]
        self.assertGreater(len(user2["username"]), len(query_username))
        response = self.app.get("/api/v1/users/search/{}/{}".format(user["user_id"], query_username),
                                data=json.dumps(user),
                                content_type='application/json')
        found_users = json.loads(response.data)["found_users"]
        self.assertEqual(len(found_users), 1)
        self.assertEqual(found_users[0]["username"], user2["username"])
