# Lo siguiente debe inicializarse en setup.py
import os
import sys

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

########
import unittest
from mock import patch
from resources.ping_resource import PingResource
from resources.ping_resource import PingSharedServerResource
from resources.ping_resource import SUCCESS_MESSAGE


class PingResourceTestCase(unittest.TestCase):

    def test_ping_app_server(self):
        service = PingResource()
        response = service.get()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, SUCCESS_MESSAGE.encode('utf-8'))

    @patch('resources.ping_resource.requests.get')
    def test_ping_shared_server(self, mock_get):
        # Configure the mock to return a response with an OK status code.
        mock_get.return_value.ok = True
        # Call the service, which will send a request to the server.
        service = PingSharedServerResource()
        response = service.get()
        # If the request is sent successfully, then I expect a response to be returned.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, SUCCESS_MESSAGE.encode('utf-8'))
