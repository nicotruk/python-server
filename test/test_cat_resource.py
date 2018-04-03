#Lo siguiente debe inicializarse en setup.py
import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
########
from resources.cat_resource import CatResource
from cats import cats
from app import app
import unittest
import json

class CatResourceTestCase(unittest.TestCase):

  def test_get_cats(self):
    service = CatResource()
    self.assertEqual(service.get(), cats)

  def test_post_cat(self):
    cat = {
      "name": "Rocky",
      "color": "blue",
      "owner": "Gonzalo",
      "weight": "3kg"
    }
    response = app.test_client().post("/api/v1/cats",
                                           data=json.dumps(cat),
                                           content_type='application/json')
    self.assertEqual(response.status_code, 200)

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
    self.assertIn(json.dumps(cat), getResponse.data)