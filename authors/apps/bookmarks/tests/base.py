from rest_framework.test import APIClient, APITestCase
from django.urls import reverse


class BaseTestCase(APITestCase):
    """
    Class to setup our tests
    """
    fixtures = ['authors/apps/bookmarks/fixtures/users.json',
                'authors/apps/bookmarks/fixtures/articles.json',
                'authors/apps/bookmarks/fixtures/bookmark.json'
                ]

    login_data = {
        "user": {
            "email": "admin@gmail.com",
            "password": "admin123456"
        }
    }

    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('user_login')
        self.login_response = self.client.post(
            self.login_url, self.login_data, format='json')
        test_token = self.login_response.data['token']
        self.auth_header = 'Bearer {}'.format(test_token)
