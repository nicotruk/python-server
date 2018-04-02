#Lo siguiente debe inicializarse en setup.py
import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
########
from resources.cat_resource import CatResource
from cats import cats
import unittest
import requests

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
  	r = requests.post('http://127.0.0.1:5000/api/v1/cats', data = cat)
  	self.assertIn(cat, cats)