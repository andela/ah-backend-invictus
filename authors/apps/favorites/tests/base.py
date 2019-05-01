from rest_framework.test import APIClient, APITestCase
from django.urls import reverse


class BaseTestCase(APITestCase):
    """ 
    Base Test class for out tests in this app
    Class will also house the setup and teardown
    methods for our tests
    """
    def setUp(self):
        # Initialize the Testclient for the tests
        self.client = APIClient()
        self.login_joel_data = {
            "user": {
                "email": "joel@gmail.com",
                "password": "?ad87654321"
            }
        }
        self.login_sanya_data = {
            "user": {
                "email": "sanyakenneth@gmail.com",
                "password": "?ad87654321"
            }
        }
        self.login_url = reverse('user_login')
        joel_response = self.client.post(
            self.login_url, self.login_joel_data, format='json')
        joel_token = joel_response.data['token']
        self.joel_auth_header = 'Bearer {}'.format(joel_token)
        sanya_response = self.client.post(
            self.login_url, self.login_sanya_data, format='json')
        sanya_token = sanya_response.data['token']
        self.sanya_auth_header = 'Bearer {}'.format(sanya_token)
