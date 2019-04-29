# Rest framework import
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
# Local import
from .test_data import TestData


class BaseTestCase(APITestCase):
    """ 
    Base Test class for out tests in this app
    Class will also house the setup and teardown
    methods for our tests
    """
    # Initialize fixture for the class Test Case
    fixtures = ['authors/apps/authentication/fixtures/signup.json']

    def setUp(self):
        # Initialize the Testclient for the tests
        self.client = APIClient()
        self.data = TestData()
        User = get_user_model()
        self.user = User.objects.create_user(
            username='test1', email='test1@example.com', password='12345678'
        )
        self.login_url = reverse('user_login')
        self.admin = User.objects.get(email="admin@gmail.com")
        setattr(self.admin, 'email_verified', True)
        self.admin.save()
        self.admin_login_response = self.client.post(
        self.login_url, self.data.login_data_admin, format='json')
        admin_test_token = self.admin_login_response.data['token']
        self.auth_header = 'Bearer {}'.format(admin_test_token)
