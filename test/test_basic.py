import mock 
import unittest

class BasicTestCase(unittest.TestCase):

	def test_basic(self):
		x = 3
		y = 3
    	self.assertEqual(x,y)