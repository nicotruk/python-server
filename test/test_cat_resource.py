from resources.cat_resource import CatResource
from cats import cats
import unittest

class CatResourceTestCase(unittest.TestCase):

  def test_get_cats(self):
    service = CatResource()
    self.assertEqual(service.get(), cats)