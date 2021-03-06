from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email="joey@gmail.com", password="111222"):
    """create a sample user"""
    return get_user_model().objects.create_user(email, password)


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

    def test_new_user_invalid_email(self):
        """test creating user without an email raises an error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "1234bb")

    def test_create_new_super_user(self):
        """ Test creating a super user """
        user = get_user_model().objects.create_superuser(
            "ayaf@gmail.com",
            "pass1122"
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(), name="Vegan"
        )

        self.assertEqual(str(tag), tag.name)
