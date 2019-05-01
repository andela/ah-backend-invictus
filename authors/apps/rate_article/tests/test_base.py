from django.urls import reverse
from rest_framework.test import APIClient, APITestCase


class BaseTestCase(APITestCase):
    """
    Base Test class for out tests in this app
    Class will also house the setup and teardown
    methods for our tests
    """

    def setUp(self):
        # Initialize the Testclient for the tests
        self.client = APIClient()
        self.login_url = reverse('user_login')
        self.login_user_edna = {
            "user": {
                "email": "3dnamargarita@gmail.com",
                "password": "@nakajugo3"
            }

        }
        self.login_user_jeoll = {
            "user": {
                "email": "joell@gmail.com",
                "password": "@nakajugo3"
            }
        }
        edna_response = self.client.post(
            self.login_url, self.login_user_edna, format='json')
        edna_token = edna_response.data['token']
        self.edna_auth_header = 'Bearer {}'.format(edna_token)

        joell_response = self.client.post(
            self.login_url, self.login_user_jeoll, format='json')
        joel_token = joell_response.data['token']
        self.joel_auth_header1 = 'Bearer {}'.format(joel_token)
