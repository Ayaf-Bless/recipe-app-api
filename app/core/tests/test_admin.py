from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="bless@gmail.com", password="1122")
        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            password="1122", email="user1@gmail.com", name="user1")

    def test_user_listed(self):
        """ test checking if users are listed """
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)