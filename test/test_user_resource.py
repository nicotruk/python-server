#Lo siguiente debe inicializarse en setup.py
import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
########
from resources.user_resource import UsersResource
from model.mongodb import db
from app import app
from mock import patch
import unittest
import json
import requests
import pprint

class UsersResourceTestCase(unittest.TestCase):

  def setUp(self):
    self.app = app.test_client() 
    self.app.testing = True

  def tearDown(self):
    with app.app_context():
      db.users.remove({})

  def test_get_all_users(self):
    response = self.app.get("/api/v1/users")
    self.assertEqual(response.status_code, 200)

  @patch('resources.user_resource.requests.post')
  def test_post_user(self, mock_post):
    mock_post.return_value.status_code = 200

    user = {
      "username": "asd",
      "password": "123",
      "email": "asd@asd.com"
    }
    response = self.app.post("/api/v1/users",
                                           data=json.dumps(user),
                                           content_type='application/json')

    userResponse = json.loads(response.data)
    user.pop('password')
    user["user_id"] = userResponse["user"]["user_id"]
    self.assertEqual(user, userResponse["user"])

  def test_get_single_user_error_user_not_found(self):
    response = self.app.get("/api/v1/users/1234")
    self.assertEqual(response.status_code, 403)
    self.assertEqual(json.loads(response.data)["message"], "There is no user with that ID!")

  @patch('resources.user_resource.requests.post')
  def test_login(self, mock_post):
    #Lo siguiente no es ideal, pero por ahora sirve. Habria que tratar de construir un objecto requests.Response
    mock_post.return_value = requests.get("http://www.mocky.io/v2/5ad6f91c2e00007800c93cb3")

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

    user = {
      "username": "asd",
      "password": "123",
      "email": "asd@asd.com"
    }
    response = self.app.post("/api/v1/users",
                                           data=json.dumps(user),
                                           content_type='application/json')

    userResponse = json.loads(response.data)
    user.pop('password')
    user["user_id"] = userResponse["user"]["user_id"]

    getResponse = self.app.get("/api/v1/users")
    self.assertIn(user, json.loads(getResponse.data)["users"])

  @patch('resources.user_resource.requests.post')
  def test_integration_get_single_user(self, mock_post):
    mock_post.return_value.status_code = 200

    user = {
      "username": "asd",
      "password": "123",
      "email": "asd@asd.com"
    }
    response = self.app.post("/api/v1/users",
                                           data=json.dumps(user),
                                           content_type='application/json')

    userResponse = json.loads(response.data)
    user.pop('password')
    user["user_id"] = userResponse["user"]["user_id"]

    getResponse = self.app.get('/api/v1/users/{}'.format(user["user_id"]))
    self.assertEqual(user,json.loads(getResponse.data)["user"])


