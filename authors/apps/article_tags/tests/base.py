from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
# Local import
from .test_data import TestData
from authors.apps.authentication.models import User


class BaseTestCase(APITestCase):
    """
    Base Test class to help setup tests for the
    article tag feature
    """
    def setUp(self):
        self.client = APIClient()
        self.data = TestData()
        self.login_url = reverse('user_login')
        self.user = User.objects.create_user(
            username="test1", email="test1@gmail.com", password="password")
        setattr(self.user, 'email_verified', True)
        self.user.save()
        self.login_data = {
            "user": {
                "email": "test1@gmail.com",
                "password": "password"
            }
        }
        self.admin_login_response = self.client.post(
        self.login_url, self.login_data, format='json')
        admin_test_token = self.admin_login_response.data['token']
        self.auth_header = 'Bearer {}'.format(admin_test_token)
