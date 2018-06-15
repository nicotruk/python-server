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
import config.firebase_config
import json

test_friendship_request = {
    "from_username": "123",
    "to_username": "456"
}

test_first_user = {
    "username": "123",
    "password": "123",
    "email": "asd@asd.com",
    "name": "Nombre Apellido",
    "firebase_token": "fdsfsdfjsdkfhsdjklhjk23h4234"
}

test_second_user = {
    "username": "456",
    "password": "456",
    "email": "asd@asd.com",
    "name": "Nombre Apellido",
    "firebase_token": "fdsfsdfjsdkfhsdjklhjk23h555"
}


class FriendshipResourceTestCase(unittest.TestCase):

    @patch('resources.user_resource.requests.post')
    def setUp(self, mock_post):
        mock_post.return_value.status_code = 200
        config.firebase_config.FIREBASE_NOTIFICATIONS_ENABLED = False
        self.app = app.test_client()
        self.app.testing = True

        user1 = test_first_user.copy()
        user2 = test_second_user.copy()

        self.app.post("/api/v1/users",
                      data=json.dumps(user1),
                      content_type='application/json')

        self.app.post("/api/v1/users",
                      data=json.dumps(user2),
                      content_type='application/json')

    def tearDown(self):
        with app.app_context():
            db.friendship_requests.delete_many({})
            db.users.delete_many({})

    def test_accept_friendship_request(self):
        friendship_request = test_friendship_request.copy()

        self.app.post("/api/v1/friendship/request",
                      data=json.dumps(friendship_request),
                      content_type='application/json')

        response = self.app.post("/api/v1/friendship",
                                 data=json.dumps(friendship_request),
                                 content_type='application/json')
        self.assertEqual(response._status_code, 201)
        friendship_response = json.loads(response.data)
        self.assertEqual(friendship_response["friendship_request"]["from_username"],
                         friendship_request["from_username"])
        self.assertEqual(friendship_response["friendship_request"]["to_username"], friendship_request["to_username"])

    @patch('resources.user_resource.requests.post')
    def test_no_friendship_request_found(self, mock_post):
        mock_post.return_value.status_code = 200
        response = {
            "token": {
                "expiresAt": "123",
                "token": "asd"
            }
        }
        mock_post.return_value.text = json.dumps(response)

        test_other_user = {
            "username": "000",
            "password": "000",
            "email": "asd@asd.com",
            "name": "Nombre Apellido",
            "firebase_token": "fdsfsdfjsdkfhsdjklhjk23h4777"
        }
        user_response = self.app.post("/api/v1/users",
                                      data=json.dumps(test_other_user),
                                      content_type='application/json')
        other_user_data = json.loads(user_response.data)

        friendship_request = test_friendship_request.copy()
        friendship_request["from_username"] = test_other_user["username"]

        response = self.app.post("/api/v1/friendship",
                                 data=json.dumps(friendship_request),
                                 content_type='application/json')

        self.assertEqual(response._status_code, 409)

        query_friends_response = self.app.get(
            '/api/v1/users/search/{}/{}'.format(other_user_data["user"]["user_id"], friendship_request["to_username"]))
        query_friends_response_data = json.loads(query_friends_response.data)
        self.assertEqual(len(query_friends_response_data["found_users"]), 0)
