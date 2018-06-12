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
import config.firebase_config

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


class FriendshipRequestResourceTestCase(unittest.TestCase):

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

    def test_create_friendship_request(self):
        friendship_request = test_friendship_request.copy()

        response = self.app.post("/api/v1/friendship/request",
                                 data=json.dumps(friendship_request),
                                 content_type='application/json')
        friendship_response = json.loads(response.data)
        self.assertEqual(friendship_request["from_username"],
                         friendship_response["friendship_request"]["from_username"])
        self.assertEqual(friendship_request["to_username"], friendship_response["friendship_request"]["to_username"])

    def test_sent_friendship_requests(self):
        friendship_request = test_friendship_request.copy()

        self.app.post("/api/v1/friendship/request",
                      data=json.dumps(friendship_request),
                      content_type='application/json')
        uri = "/api/v1/friendship/request/sent/" + friendship_request["from_username"]
        response = self.app.get(uri,
                                content_type='application/json')
        friendship_response = json.loads(response.data)
        self.assertEqual(len(friendship_response["friendship_requests"]), 1)
        self.assertEqual(friendship_response["friendship_requests"][0]["from_username"],
                         friendship_request["from_username"])

    def test_received_friendship_requests(self):
        friendship_request = test_friendship_request.copy()

        self.app.post("/api/v1/friendship/request",
                      data=json.dumps(friendship_request),
                      content_type='application/json')
        uri = "/api/v1/friendship/request/received/" + friendship_request["to_username"]
        response = self.app.get(uri,
                                content_type='application/json')
        friendship_response = json.loads(response.data)
        self.assertEqual(len(friendship_response["friendship_requests"]), 1)
        self.assertEqual(friendship_response["friendship_requests"][0]["to_username"],
                         friendship_request["to_username"])
