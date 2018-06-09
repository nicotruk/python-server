# Lo siguiente debe inicializarse en setup.py
import os
import sys

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
########
from config.mongodb import db
from app import app
import unittest
import json
import config.firebase_config

test_direct_message = {
    "from_username": "123",
    "to_username": "456",
    "message": "Hello!"
}


class DirectMessageResourceTestCase(unittest.TestCase):

    def setUp(self):
        config.firebase_config.FIREBASE_NOTIFICATIONS_ENABLED = False
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        with app.app_context():
            db.direct_messages.delete_many({})

    def test_create_direct_message(self):
        direct_message = test_direct_message.copy()

        response = self.app.post("/api/v1/direct_message",
                                 data=json.dumps(direct_message),
                                 content_type='application/json')
        direct_message_response = json.loads(response.data)
        direct_message_response["direct_message"].pop("_id")
        direct_message_response["direct_message"].pop("timestamp")
        self.assertEqual(direct_message, direct_message_response["direct_message"])

    def test_received_messages(self):
        direct_message = test_direct_message.copy()

        self.app.post("/api/v1/direct_message",
                      data=json.dumps(direct_message),
                      content_type='application/json')
        uri = "/api/v1/direct_message/received/" + direct_message["to_username"]
        response = self.app.get(uri,
                                content_type='application/json')
        direct_message_response = json.loads(response.data)
        self.assertEqual(len(direct_message_response["direct_messages"]), 1)
        self.assertEqual(direct_message_response["direct_messages"][0]["to_username"],
                         direct_message["to_username"])

    def test_user_messages_count(self):
        direct_message = test_direct_message.copy()
        self.app.post("/api/v1/direct_message",
                      data=json.dumps(direct_message),
                      content_type='application/json')

        other_test_direct_message = {
            "from_username": direct_message["to_username"],
            "to_username": direct_message["from_username"],
            "message": "Hi! How are you?"
        }
        self.app.post("/api/v1/direct_message",
                      data=json.dumps(other_test_direct_message),
                      content_type='application/json')

        uri = "/api/v1/direct_message/" + direct_message["to_username"]
        response = self.app.get(uri,
                                content_type='application/json')
        direct_message_response = json.loads(response.data)
        self.assertEqual(len(direct_message_response["direct_messages"]), 1)

    def test_user_messages(self):
        direct_message = test_direct_message.copy()
        self.app.post("/api/v1/direct_message",
                      data=json.dumps(direct_message),
                      content_type='application/json')

        other_test_direct_message = {
            "from_username": direct_message["to_username"],
            "to_username": "otro",
            "message": "Hi! How are you?"
        }
        self.app.post("/api/v1/direct_message",
                      data=json.dumps(other_test_direct_message),
                      content_type='application/json')

        uri = "/api/v1/direct_message/" + direct_message["to_username"]
        response = self.app.get(uri,
                                content_type='application/json')
        direct_message_response = json.loads(response.data)
        self.assertEqual(len(direct_message_response["direct_messages"]), 2)
        self.assertLessEqual(direct_message_response["direct_messages"][0]["timestamp"],
                             direct_message_response["direct_messages"][1]["timestamp"])

    def test_conversation_messages(self):
        direct_message = test_direct_message.copy()
        self.app.post("/api/v1/direct_message",
                      data=json.dumps(direct_message),
                      content_type='application/json')

        other_test_direct_message = {
            "from_username": direct_message["to_username"],
            "to_username": direct_message["from_username"],
            "message": "Hi! How are you?"
        }
        self.app.post("/api/v1/direct_message",
                      data=json.dumps(other_test_direct_message),
                      content_type='application/json')

        other_test_direct_message = {
            "from_username": direct_message["to_username"],
            "to_username": "otro",
            "message": "Hi! How are you?"
        }
        self.app.post("/api/v1/direct_message",
                      data=json.dumps(other_test_direct_message),
                      content_type='application/json')

        uri = "/api/v1/direct_message/conversation/" + direct_message["from_username"] + "/" + direct_message[
            "to_username"]
        response = self.app.get(uri,
                                content_type='application/json')
        direct_message_response = json.loads(response.data)
        self.assertEqual(len(direct_message_response["direct_messages"]), 2)
        users = [direct_message["from_username"], direct_message["to_username"]]
        self.assertIn(direct_message_response["direct_messages"][0]["from_username"], users)
        self.assertIn(direct_message_response["direct_messages"][0]["to_username"], users)
        self.assertIn(direct_message_response["direct_messages"][1]["from_username"], users)
        self.assertIn(direct_message_response["direct_messages"][1]["to_username"], users)
        self.assertLessEqual(direct_message_response["direct_messages"][0]["timestamp"],
                             direct_message_response["direct_messages"][1]["timestamp"])
