from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from authors.apps.profiles.models import UserProfile

User = get_user_model()


class BaseTestCase(APITestCase):
    """
    Testcases base for the user profile views.
    """

    def setUp(self):
        """Initialize test client."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='test1', email='test1@example.com', password='12345678'
        )
        setattr(self.user, 'email_verified', True)
        self.user.save()
        self.data = {
            'user':
                {
                    'email': 'test1@example.com', 'password': '12345678'
                }
            }
        self.login = reverse('user_login')
        self.login_response = self.client.post(
            self.login, self.data, format="json")
        user_token = self.login_response.data['token']
        self.auth_header = 'Bearer {}'.format(user_token)

        self.profile = {
            "profile": {
                "firstname": "isaac",
                "lastname": "kimbugwe",
                "username": "isaac3",
                "image": "http://127.0.0.1:8000/api/users/profile/isaac.png",
                "bio": "I work at Andela"
            }
        }
        self.profile2 = {
            "profile": {
                "firstname": "isaac1",
                "lastname": "kimbugwe1",
                "username": "isaac1",
                "image": "http://127.0.0.1:8000/api/users/profile/isaac1.png",
                "bio": "I work at Andela uganda"
            }
        }
        self.profile4 = {
            "profile": {
                "firstname": "isaac1",
                "lastname": "kim",
                "username": "isaac12",
                "image": "http://127.0.0.1:8000/api/users/profile/isaac12.png",
                "bio": "I work at Andela uganda..."
            }
        }
        self.profile3 = {
            "profile": {
                "firstname": "is",
                "lastname": "kimbugwe12",
                "username": "isaac12",
                "image": "http://127.0.0.1:8000/api/users/profile/isaac12.png",
                "bio": "I work at Andela uganda..."
            }
        }
        self.profile5 = {
            "profile": {
                "firstname": "isaac23",
                "lastname": "kimbugwe12",
                "username": "is",
                "image": "http://127.0.0.1:8000/api/users/profile/isaac12.png",
                "bio": "I work at Andela uganda..."
            }
        }
        self.user2 = User.objects.create_user(
            username='test2', email='test2@example.com', password='12345678'
        )
        setattr(self.user2, 'email_verified', True)
        self.user2.save()
        self.data2 = {
            'user': {
                'email': 'test2@example.com', 'password': '12345678'
            }
        }
