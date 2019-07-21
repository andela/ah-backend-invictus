from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase, APIClient

from authors.apps.articles.models import Article
from authors.apps.comments.models import Comment

User = get_user_model()


class BaseTestCase(APITestCase):
    """
    Testcases base for the comment API views.
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

        self.user2 = User.objects.create_user(
            username='test12', email='test12@example.com', password='123456789'
        )
        setattr(self.user2, 'email_verified', True)
        self.user2.save()
        self.data = {
            'user':
                {
                    'email': 'test12@example.com', 'password': '123456789'
                }
            }
        self.login = reverse('user_login')
        self.login_response = self.client.post(
            self.login, self.data, format="json")
        user_token2 = self.login_response.data['token']
        self.auth_header2 = 'Bearer {}'.format(user_token2)

        self.article = Article.objects.create(
            id=1,
            title='Town hall at Andela',
            description='There was lots of fun',
            body='There was no TIA chant.',
            author=self.user
        )
        self.article2 = Article.objects.create(
            id=2,
            title='Town hall at Andela',
            description='There was lots of fun',
            body='There was no TIA chant.',
            author=self.user
        )
        self.comment_data = Comment.objects.create(
            id=100,
            body="Heheheheheh ehehehehe.....",
            article=self.article,
            author=self.user
        )
        self.comment = {
            "comment": {
                "body": "His name was my name too.",
            }
        }
        self.comment2 = {
            "comment": {
                "body": "His name was my name too..."
            }
        }
        self.comment3 = {
            "comment": {
                "body": "His name was my name too...XYZ"
            }
        }
        self.comment_text = {
            "comment": {
                "body": "This is sample text.",
                "first_index": 1,
                "last_index": 7,
                "highlighted_text": "This is "
            }
        }
        self.comment_text1 = {
            "comment": {
                "body": "This is sample text.",
                "first_index": "1",
                "last_index": 7,
                "highlighted_text": "This is "
            }
        }
        self.comment_text2 = {
            "comment": {
                "body": "This is sample text.",
                "first_index": 1,
                "last_index": "7",
                "highlighted_text": "This is "
            }
        }
        self.comment_text3 = {
            "comment": {
                "body": "This is sample text.",
                "first_index": 100,
                "last_index": 200,
                "highlighted_text": "This is sample text."
            }
        }
        self.comment_text4 = {
            "comment": {
                "body": "This is sample text.",
                "first_index": 20,
                "last_index": 10,
                "highlighted_text": "This is sample text."
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
