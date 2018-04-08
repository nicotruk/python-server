#Lo siguiente debe inicializarse en setup.py
import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
########
from resources.user_resource import UsersResource
from app import app
import unittest
import json
import pprint

class UsersResourceTestCase(unittest.TestCase):

  def test_get_all_users(self):
    response = app.test_client().get("/api/v1/users")
    self.assertEqual(response.status_code, 200)

  def test_post_user(self):
    user = {
      "username": "asd",
      "password": "1234",
      "email": "asd@asd.com"
    }
    response = app.test_client().post("/api/v1/users",
                                           data=json.dumps(user),
                                           content_type='application/json')
    userResponse = json.loads(response.data)
    user["user_id"] = userResponse["user"]["user_id"]
    self.assertEqual(user, userResponse["user"])

  def test_get_single_user_error_user_not_found(self):
    response = app.test_client().get("/api/v1/users/1234")
    self.assertEqual(response.status_code, 403)
    self.assertEqual(json.loads(response.data)["message"], "There is no user with that ID!")
    
  def test_integration_create_user(self):
    user = {
      "username": "asd",
      "password": "1234",
      "email": "asd@asd.com"
    }
    response = app.test_client().post("/api/v1/users",
                                           data=json.dumps(user),
                                           content_type='application/json')

    userResponse = json.loads(response.data)
    user["user_id"] = userResponse["user"]["user_id"]

    getResponse = app.test_client().get("/api/v1/users")
    self.assertIn(user, json.loads(getResponse.data)["users"])

  def test_integration_get_single_user(self):
    user = {
      "username": "asd",
      "password": "1234",
      "email": "asd@asd.com"
    }
    response = app.test_client().post("/api/v1/users",
                                           data=json.dumps(user),
                                           content_type='application/json')

    userResponse = json.loads(response.data)
    user["user_id"] = userResponse["user"]["user_id"]

    getResponse = app.test_client().get('/api/v1/users/{}'.format(user["user_id"]))
    self.assertEqual(user,json.loads(getResponse.data)["user"])



