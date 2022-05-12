from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """Test the users API (public)"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            "email": "ayaf@gmail.com",
            "password": "11005",
            "name": "ayaf"
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_user_exist(self):
        """Test check if the user already exist and fails"""
        payload = {
            "email": "ayaf@gmail.com",
            "password": "11040",
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that password is at least 5 character"""
        payload = {
            "email": "ayaf@gmail.com",
            "password": "ps",
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exist = get_user_model().objects.filter(
            email=payload["email"]
        ).exists()
        self.assertFalse(user_exist)

    def test_create_token_for_user(self):
        """Test that the token is created for the user"""
        payload = {
            "email": "ayaf@gmail.com",
            "password": "password",
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("token", res.data)

    def test_create_token_invalid_credentials(self):
        """Test that the token is not created if the data are not valid"""
        create_user(email="bless@gmail.com", password="11223")
        payload = {
            "email": "bless@gmail.com",
            "password": "wrong-password"
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test token is not created if the user does not exist"""
        payload = {
            "email": "bless@gmail.com",
            "password": "password"
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_fields(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {"email": "one", "password": ""})
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
