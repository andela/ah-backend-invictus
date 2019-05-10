from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from authors.apps.authentication.models import User
from authors.apps.pushnotifications.models import PushNotification

class BaseTestCase(APITestCase):
    """ 
    Base Test class for out tests in this app
    Class will also house the setup and teardown
    """

    def setUp(self):
        # Initialize the Testclient for the tests
        self.client = APIClient()

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

        self.user2 = User.objects.create_user(
            username="marcus", email="marcus@gmail.com", password="marcusPassword1234")
        setattr(self.user2, 'email_verified', True)
        self.user2.save()

        self.user2_login_data = {
            "user": {
                "email": "marcus@gmail.com",
                "password": "marcusPassword1234"
            }
        }

        self.user2_login_response = self.client.post(
            self.login_url, self.user2_login_data, format='json')
        user2_token = self.user2_login_response.data['token']
        self.auth_header2 = 'Bearer {}'.format(user2_token)

        self.create_article_data = {
            "title": "Fresh kid wonders on stage at lugogo",
            "description": "he wows the kids",
            "body": "Fresh kid is a 5 year musician who has been on map.",
            "author": self.user.username,
            "tagList": []
        }
        self.comment = {
            "comment": {
                "body": "His name was my name too."
            }
        }

        self.pushnotification=PushNotification.objects.create(
            id=20,
            message="Your article with title 'Hello Andela has been favorited",
            receiver=self.user2
        )
        