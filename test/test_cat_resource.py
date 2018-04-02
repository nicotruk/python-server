#Lo siguiente debe inicializarse en setup.py
import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
########
from resources.cat_resource import CatResource
from cats import cats
from app import app
import unittest

class CatResourceTestCase(unittest.TestCase):

  def test_get_cats(self):
    service = CatResource()
    self.assertEqual(service.get(), cats)

  def test_post_cat(self):
  	service = CatResource()
  	cat = {
      "name": "Rocky",
      "color": "blue",
      "owner": "Gonzalo",
      "weight": "3kg"
    }
      test_app = app.test_client()
  	   result = test_app.post("/api/v1/cats",
                                  data=cat,
                                  content_type='application/json')
  	self.assertIn(cat, service.get())