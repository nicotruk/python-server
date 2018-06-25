# Lo siguiente debe inicializarse en setup.py
import os
import sys

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

########
import unittest
from mock import patch
from resources.ping_resource import SUCCESS_MESSAGE
from app import app
from config.mongodb import db


class PingResourceTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        with app.app_context():
            db.requests_stats.delete_many({})

    @patch('resources.ping_resource.current_app')
    def test_ping_app_server(self, mock_app):
        response = self.app.get("/api/v1/ping")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, SUCCESS_MESSAGE.encode('utf-8'))

    @patch('resources.ping_resource.requests.get')
    @patch('resources.ping_resource.current_app')
    def test_ping_shared_server(self, mock_get, mock_app):
        # Configure the mock to return a response with an OK status code.
        mock_get.return_value.ok = True
        # Call the service, which will send a request to the server.
        response = self.app.get("/api/v1/ping/sharedServer")
        # If the request is sent successfully, then I expect a response to be returned.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, SUCCESS_MESSAGE.encode('utf-8'))
