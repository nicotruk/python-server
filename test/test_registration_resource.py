# Lo siguiente debe inicializarse en setup.py
import os
import sys

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

########
import unittest
import json
from mock import patch
from app import app


class RegistrationResourceTestCase(unittest.TestCase):

    @patch('resources.user_resource.requests.post')
    def test_ping_shared_server(self, mock_post):
        # Configure the mock to return a response with an OK status code.
        mock_post.return_value.status_code = 200
        # Call the service, which will send a request to the server.
        user_data = {
            "username": "nico",
            "password": "1234"
        }
        response = app.test_client().post("/api/v1/login", data=json.dumps(user_data), content_type='application/json')
        # If the request is sent successfully, then I expect a response to be returned.
        self.assertEqual(response.status_code, 200)
