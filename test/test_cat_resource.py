import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
from resources.cat_resource import CatResource
from cats import cats
import unittest

class CatResourceTestCase(unittest.TestCase):

  def test_get_cats(self):
    service = CatResource()
    self.assertEqual(service.get(), cats)