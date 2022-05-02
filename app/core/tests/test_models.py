from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTest(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email"""
        email = "ayaf@gmail.com"
        password = "testPass11"
        user = get_user_model().objects.create_user(
            email=email, password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalize(self):
        """Test the new user email is normalized"""
        email = "ayaf@GMAIL.COM"
        user = get_user_model().objects.create_user(email, "12345")
        self.assertEqual(user.email, email.lower())
