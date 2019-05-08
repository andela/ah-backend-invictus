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

        self.user2 = User.objects.create_superuser(
            username="superuser", email="super@gmail.com", password="SuperPassword1234")
        setattr(self.user2, 'email_verified', True)
        self.user2.save()

        self.super_login_data = {
            "user": {
                "email": "super@gmail.com",
                "password": "SuperPassword1234"
            }
        }

        self.super_login_response = self.client.post(
            self.login_url, self.super_login_data, format='json')
        super_test_token = self.super_login_response.data['token']
        self.super_auth_header = 'Bearer {}'.format(super_test_token)

        self.create_article_data = {
            "title": "Fresh kid wonders on stage at lugogo",
            "description": "he wows the kids",
            "body": "Fresh kid is a 5 year musician who has been on map.",
            "author": self.user.username,
            "tagList": []
        }
        self.create_article_with_blank_title = {
            "title": "",
            "description": "he wows the kids",
            "body": "Fresh kid is a 5 year musician who has been on map.",
            "tagList": []
        }
        self.create_article_with_no_title = {
            "description": "he wows the kids",
            "body": "Fresh kid is a 5 year musician who has been on map.",
            "tagList": []
        }
        self.create_article_with_blank_description = {
            "title": "fresh kid is a wiz",
            "description": "",
            "body": "Fresh kid is a 5 year musician who has been on map.",
            "tagList": []
        }
        self.create_article_with_no_description = {
            "title": "he wows the kids",
            "body": "Fresh kid is a 5 year musician who has been on map.",
            "tagList": []
        }
        self.create_article_with_blank_body = {
            "title": "fresh kid is a wiz",
            "description": "Fresh kid is a 5 year musician who has been on map",
            "body": "",
            "tagList": []
        }
        self.create_article_with_no_body = {
            "title": "he wows the kids",
            "bdescription": "Fresh kid is a 5 year musician who has been on map.",
            "tagList": []
        }

        self.update_article = {
            "title": "Fresh kid concert was great",
            "description": "he wowed the adults too",
            "body": "Fresh kid is on the map.",
            "tagList": []
        }
        self.short_title_article = {
            "title": "F",
            "description": "he wowed the adults too",
            "body": "Fresh kid is on the map.",
            "tagList": []
        }

        self.create_article_user = {
            "title": "Town hall at Andela",
            "description": "There was lots of fun",
            "body": "There was no TIA chant.",
            "tagList": []
        }
        self.article_with_tag = {
            "title": "Fresh kid wonders on stage at lugogo",
            "description": "he wows the kids",
            "body": "Fresh kid is a 5 year musician who has been on map.",
            "author": self.user.username,
            "tagList": ["edna"]
        }

        self.report = {
            "report": {
                "reason": "Plagiarism. He stole intellectual property and refused to site"
            }
        }

        self.report_with_blank_reason = {
            "report": {
                "reason": ""
            }
        }

        self.report_with_no_reason = {
            "report": {
            }
        }
