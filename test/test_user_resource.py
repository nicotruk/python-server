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
  def test_post_user(self):
    mock_post.return_value.ok = True

    user = {
      "username": "asd",
      "email": "asd@asd.com"
    }
    response = self.app.post("/api/v1/users",
                                           data=json.dumps(user),
                                           content_type='application/json')
    userResponse = json.loads(response.data)
    user["user_id"] = userResponse["user"]["user_id"]
    self.assertEqual(user, userResponse["user"])

  def test_get_single_user_error_user_not_found(self):
    response = self.app.get("/api/v1/users/1234")
    self.assertEqual(response.status_code, 403)
    self.assertEqual(json.loads(response.data)["message"], "There is no user with that ID!")
    
  @patch('resources.user_resource.requests.post')
  def test_integration_create_user(self):
    mock_post.return_value.ok = True

    user = {
      "username": "asd",
      "email": "asd@asd.com"
    }
    response = self.app.post("/api/v1/users",
                                           data=json.dumps(user),
                                           content_type='application/json')

    userResponse = json.loads(response.data)
    user["user_id"] = userResponse["user"]["user_id"]

    getResponse = self.app.get("/api/v1/users")
    self.assertIn(user, json.loads(getResponse.data)["users"])

  @patch('resources.user_resource.requests.post')
  def test_integration_get_single_user(self):
    mock_post.return_value.ok = True

    user = {
      "username": "asd",
      "email": "asd@asd.com"
    }
    response = self.app.post("/api/v1/users",
                                           data=json.dumps(user),
                                           content_type='application/json')

    userResponse = json.loads(response.data)
    user["user_id"] = userResponse["user"]["user_id"]

    getResponse = self.app.get('/api/v1/users/{}'.format(user["user_id"]))
    self.assertEqual(user,json.loads(getResponse.data)["user"])


