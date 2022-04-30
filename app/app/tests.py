from django.test import TestCase

from .calc import add


class CalcTest(TestCase):
    def test_add_number(self):
        """Test that two numbers are added together"""
        self.assertEqual(add(2, 1), 5)
