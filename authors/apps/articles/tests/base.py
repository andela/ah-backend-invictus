from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from authors.apps.authentication.models import User


class BaseTestCase(APITestCase):
    """ 
    Base Test class for out tests in this app
    Class will also house the setup and teardown
    methods for our tests
    """

    def setUp(self):
        # Initialize the Testclient for the tests
        self.client = APIClient()


        self.login_url = reverse('authentication:user_login')

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

        self.create_article_data = {
            "title": "Fresh kid wonders on stage at lugogo",
            "description": "he wows the kids",
            "body": "Fresh kid is a 5 year musician who has been on map.",
            "author": self.user.username
        }
        self.create_article_with_blank_title = {
            "title": "",
            "description": "he wows the kids",
            "body": "Fresh kid is a 5 year musician who has been on map."
        }
        self.create_article_with_no_title = {
            "description": "he wows the kids",
            "body": "Fresh kid is a 5 year musician who has been on map."
        }
        self.create_article_with_blank_description = {
            "title": "fresh kid is a wiz",
            "description": "",
            "body": "Fresh kid is a 5 year musician who has been on map."
        }
        self.create_article_with_no_description = {
            "title": "he wows the kids",
            "body": "Fresh kid is a 5 year musician who has been on map."
        }
        self.create_article_with_blank_body = {
            "title": "fresh kid is a wiz",
            "description": "Fresh kid is a 5 year musician who has been on map",
            "body": ""
        }
        self.create_article_with_no_body = {
            "title": "he wows the kids",
            "bdescription": "Fresh kid is a 5 year musician who has been on map."
        }

        self.update_article = {
            "title": "Fresh kid concert was great",
            "description": "he wowed the adults too",
            "body": "Fresh kid is on the map."
        }
        self.short_title_article = {
            "title": "F",
            "description": "he wowed the adults too",
            "body": "Fresh kid is on the map."
        }

        self.create_article_user = {
            "title": "Town hall at Andela",
            "description": "There was lots of fun",
            "body": "There was no TIA chant."
        }
