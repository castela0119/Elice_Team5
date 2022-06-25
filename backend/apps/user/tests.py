from backend.apps.user.models import User
from django.urls import reverse
from rest_framework import status

# from rest_framework_simplejwt.models import TokenUser
# from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class RegisterTestCase(APITestCase):
    def test_register_ok(self):
        data = {
            "user_ID": "testcase",
            "email": "testcase@example.com",
            "password": "NewPassword123",
        }
        response = self.client.post(reverse("register"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            user_ID="example", email="example@example.com", password="newPassword@123"
        )

    def test_obtain_tokens_ok(self):
        data = {
            "user_ID": "example",
            "password": "newPassword@123",
        }
        response = self.client.post(reverse("token_obtain_pair"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
