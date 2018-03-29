import mock 
import unittest

class BasicTestCase(unittest.TestCase):

	@given(st.integers(), st.integers())
	def test_ints_are_commutative(x, y):
    	assert x + y == y + x