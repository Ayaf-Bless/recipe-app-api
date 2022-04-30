from django.test import TestCase

from .calc import add, subtract


class CalcTest(TestCase):
    def test_add_number(self):
        """Test that two numbers are added together"""
        self.assertEqual(add(2, 1), 3)

    def test_subtract_number(self):
        """Test that two numbers are added together"""
        self.assertEqual(subtract(8, 2), 6)
