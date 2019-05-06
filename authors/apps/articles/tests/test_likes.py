# Django and Rest framework imports
from django.urls import reverse
from rest_framework import status
# Local imports
from .base import BaseTestCase
from authors.apps.authentication.models import User


class LikesTest(BaseTestCase):
    """
    Class Test Case for Testing like and dislike functionality
    """

    def test_user_like_article_status(self):
        """
        Method tests the status on like article response
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_data, HTTP_AUTHORIZATION=self.auth_header, format="json")
        article_id = response.data['article']['id']
        url = '/api/articles/{}/like/'.format(article_id)
        response = self.client.post(
            url, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_like_article_message(self):
        """
        Method tests liking the article response message
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_data, HTTP_AUTHORIZATION=self.auth_header, format="json")
        article_id = response.data['article']['id']
        url = '/api/articles/{}/like/'.format(article_id)
        response = self.client.post(
            url, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.data['success'],
                         "You have successfully liked this article.")

    def test_user_like_article_twice_status(self):
        """
        Method tests liking article twice status code
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_data, HTTP_AUTHORIZATION=self.auth_header, format="json")
        article_id = response.data['article']['id']
        url = '/api/articles/{}/like/'.format(article_id)
        response = self.client.post(
            url, HTTP_AUTHORIZATION=self.auth_header, format="json")
        response = self.client.post(
            url, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_like_article_twice_error_message(self):
        """
        Method tests liking article twice error message
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_data, HTTP_AUTHORIZATION=self.auth_header, format="json")
        article_id = response.data['article']['id']
        url = '/api/articles/{}/like/'.format(article_id)
        response = self.client.post(
            url, HTTP_AUTHORIZATION=self.auth_header, format="json")
        response = self.client.post(
            url, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.data['message'],
                         "Your like has been revoked")

    def test_user_dislike_article_status(self):
        """
        Method tests the status on dislike article response
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_data, HTTP_AUTHORIZATION=self.auth_header, format="json")
        article_id = response.data['article']['id']
        url = '/api/articles/{}/dislike/'.format(article_id)
        response = self.client.post(
            url, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_dislike_article_message(self):
        """
        Method tests disliking the article response message
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_data, HTTP_AUTHORIZATION=self.auth_header, format="json")
        article_id = response.data['article']['id']
        url = '/api/articles/{}/dislike/'.format(article_id)
        response = self.client.post(
            url, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(
            response.data['success'], "You have successfully disliked this article.")

    def test_user_dislike_article_twice_status(self):
        """
        Method tests disliking article twice status code
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_data, HTTP_AUTHORIZATION=self.auth_header, format="json")
        article_id = response.data['article']['id']
        url = '/api/articles/{}/dislike/'.format(article_id)
        response = self.client.post(
            url, HTTP_AUTHORIZATION=self.auth_header, format="json")
        response = self.client.post(
            url, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_dislike_article_twice_error_message(self):
        """
        Method tests disliking article twice error message
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_data, HTTP_AUTHORIZATION=self.auth_header, format="json")
        article_id = response.data['article']['id']
        url = '/api/articles/{}/dislike/'.format(article_id)
        response = self.client.post(
            url, HTTP_AUTHORIZATION=self.auth_header, format="json")
        response = self.client.post(
            url, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.data['message'],
                         "Your dislike has been revoked")

    def test_user_like_article_not_found(self):
        """
        Method tests response for like of article not found
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_data, HTTP_AUTHORIZATION=self.auth_header, format="json")
        url = 'api/articles/100000/like'
        response = self.client.post(
            url, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_like_then_dislike_article(self):
        """
        Method tests liking then disliking the article
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_data, HTTP_AUTHORIZATION=self.auth_header, format="json")
        article_id = response.data['article']['id']
        url = '/api/articles/{}/like/'.format(article_id)
        response = self.client.post(
            url, HTTP_AUTHORIZATION=self.auth_header, format="json")
        url = '/api/articles/{}/dislike/'.format(article_id)
        response = self.client.post(
            url, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.data['success'],
                         "Your like for the article has changed to a dislike.")

    def test_user_dislike_then_like_article(self):
        """
        Method tests disliking then liking the article
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_data, HTTP_AUTHORIZATION=self.auth_header, format="json")
        article_id = response.data['article']['id']
        url = '/api/articles/{}/dislike/'.format(article_id)
        response = self.client.post(
            url, HTTP_AUTHORIZATION=self.auth_header, format="json")
        url = '/api/articles/{}/like/'.format(article_id)
        response = self.client.post(
            url, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.data['success'],
                         "Your dislike for the article has changed to a like.")

    def test_user_dislike_then_like_article_status(self):
        """
        Method tests disliking then liking the article status code
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_data, HTTP_AUTHORIZATION=self.auth_header, format="json")
        article_id = response.data['article']['id']
        url = '/api/articles/{}/dislike/'.format(article_id)
        response = self.client.post(
            url, HTTP_AUTHORIZATION=self.auth_header, format="json")
        url = '/api/articles/{}/like/'.format(article_id)
        response = self.client.post(
            url, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_like_then_dislike_article_status(self):
        """
        Method tests disliking then liking the article status response
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_data, HTTP_AUTHORIZATION=self.auth_header, format="json")
        article_id = response.data['article']['id']
        url = '/api/articles/{}/like/'.format(article_id)
        response = self.client.post(
            url, HTTP_AUTHORIZATION=self.auth_header, format="json")
        url = '/api/articles/{}/dislike/'.format(article_id)
        response = self.client.post(
            url, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
