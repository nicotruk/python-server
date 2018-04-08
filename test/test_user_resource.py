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
    pprint.pprint(response)
    self.assertEqual(response.status_code, 200)

    '''
  def test_integration_create_cat(self):
    cat = {
      "name": "Rocky",
      "color": "blue",
      "owner": "Gonzalo",
      "weight": "3kg"
    }
    response = app.test_client().post("/api/v1/cats",
                                           data=json.dumps(cat),
                                           content_type='application/json')
    getResponse = app.test_client().get("/api/v1/cats")
    self.assertIn(cat, json.loads(getResponse.data))

    '''