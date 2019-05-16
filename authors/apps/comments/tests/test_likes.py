import json
from rest_framework.test import APIClient, APITestCase
from authors.apps.authentication.models import User
from authors.apps.comments.tests.base import BaseTestCase
from django.urls import reverse
from rest_framework import status

class TestLikeCommment(BaseTestCase):
    """Class to test like and unlike a comment."""

    def test_user_to_like_own_comment(self):
        """Test post a comment on an article and like a comment."""
        url = reverse('comment_list', kwargs={'article_id': 1})
        response = self.client.post(url, self.comment,
                                    HTTP_AUTHORIZATION=self.auth_header,
                                    format="json")
        comment_id = response.data['comment']['id']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url1 = reverse('like_comment', kwargs={'article_id':1, 'comment_id':comment_id})
        response1 = self.client.post(url1,
                                    HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response1.status_code, 403)

    def test_user_to_like_missing_comment(self):
        """Test liking a comment that does not exist."""
        url = reverse('like_comment', kwargs={'article_id':1, 'comment_id':0})
        response1 = self.client.post(url,
                                    HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response1.status_code, 404)

    def test_user_liking_your_own_comment(self):
        """Test liking your own comment."""
        url = reverse('comment_list', kwargs={'article_id': 1})
        response = self.client.post(url, self.comment,
                                    HTTP_AUTHORIZATION=self.auth_header,
                                    format="json")
        comment_id = response.data['comment']['id']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url1 = reverse('like_comment', kwargs={'article_id':1, 'comment_id':comment_id})
        response1 = self.client.post(url1,
                                    HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response1.data['message'], "You can not like your own comment.")

    def test_user_to_liking_another_comment(self):
        """Test liking your own comment."""
        url = reverse('comment_list', kwargs={'article_id': 1})
        response = self.client.post(url, self.comment,
                                    HTTP_AUTHORIZATION=self.auth_header,
                                    format="json")
        comment_id = response.data['comment']['id']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url1 = reverse('like_comment', kwargs={'article_id':1, 'comment_id':comment_id})
        response1 = self.client.post(url1,
                                    HTTP_AUTHORIZATION=self.auth_header2, format="json")
        self.assertEqual(response1.status_code, 200)

    def test_user_to_like_another_comment(self):
        """Test liking another comment."""
        url = reverse('comment_list', kwargs={'article_id': 1})
        response = self.client.post(url, self.comment,
                                    HTTP_AUTHORIZATION=self.auth_header,
                                    format="json")
        comment_id = response.data['comment']['id']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url1 = reverse('like_comment', kwargs={'article_id':1, 'comment_id':comment_id})
        response1 = self.client.post(url1,
                                    HTTP_AUTHORIZATION=self.auth_header2, format="json")
        self.assertEqual(response1.data['success'], "You have successfully liked this comment.")
        self.assertEqual(response1.status_code, 200)

    def test_user_to_like_twice_a_comment(self):
        """Test liking your own comment."""
        url = reverse('comment_list', kwargs={'article_id': 1})
        response = self.client.post(url, self.comment,
                                    HTTP_AUTHORIZATION=self.auth_header,
                                    format="json")
        comment_id = response.data['comment']['id']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url1 = reverse('like_comment', kwargs={'article_id':1, 'comment_id':comment_id})
        response1 = self.client.post(url1,
                                    HTTP_AUTHORIZATION=self.auth_header2, format="json")
        response1 = self.client.post(url1,
                                    HTTP_AUTHORIZATION=self.auth_header2, format="json")
        self.assertEqual(response1.data['message'], "Your like has been cancelled")
        self.assertEqual(response1.status_code, 200)

    def test_user_has_not_liked_a_comment(self):
        """Test a user has ever liked a comment."""
        url = reverse('comment_list', kwargs={'article_id': 1})
        response = self.client.post(url, self.comment,
                                    HTTP_AUTHORIZATION=self.auth_header,
                                    format="json")
        comment_id = response.data['comment']['id']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url1 = reverse('get_likes', kwargs={'article_id':1, 'comment_id':comment_id})
        response1 = self.client.get(url1,
                                    HTTP_AUTHORIZATION=self.auth_header2, format="json")
        self.assertIn('False', str(response1.data))

    def test_user_has_not_liked_comment(self):
        """Test a user has never liked a comment using status code."""
        url = reverse('comment_list', kwargs={'article_id': 1})
        response = self.client.post(url, self.comment,
                                    HTTP_AUTHORIZATION=self.auth_header,
                                    format="json")
        comment_id = response.data['comment']['id']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url1 = reverse('get_likes', kwargs={'article_id':1, 'comment_id':comment_id})
        response1 = self.client.get(url1,
                                    HTTP_AUTHORIZATION=self.auth_header2, format="json")
        self.assertEqual(response1.status_code, 200)

    def test_user_has_liked_comment(self):
        """Test a user has ever liked a comment using status code."""
        url = reverse('comment_list', kwargs={'article_id': 1})
        response = self.client.post(url, self.comment,
                                    HTTP_AUTHORIZATION=self.auth_header,
                                    format="json")
        comment_id = response.data['comment']['id']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url0 = reverse('like_comment', kwargs={'article_id':1, 'comment_id':comment_id})
        url1 = reverse('get_likes', kwargs={'article_id':1, 'comment_id':comment_id})
        response2 = response.client.post(url0,
                                    HTTP_AUTHORIZATION=self.auth_header2, format="json")
        response1 = self.client.get(url1,
                                    HTTP_AUTHORIZATION=self.auth_header2, format="json")
        self.assertEqual(response1.status_code, 200)
        self.assertIn('True', str(response1.data))

    def test_user_has_likes_comment(self):
        """Test a user has ever liked a comment using message."""
        url = reverse('comment_list', kwargs={'article_id': 1})
        response = self.client.post(url, self.comment,
                                    HTTP_AUTHORIZATION=self.auth_header,
                                    format="json")
        comment_id = response.data['comment']['id']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url0 = reverse('like_comment', kwargs={'article_id':1, 'comment_id':comment_id})
        url1 = reverse('get_likes', kwargs={'article_id':1, 'comment_id':comment_id})
        response2 = response.client.post(url0,
                                    HTTP_AUTHORIZATION=self.auth_header2, format="json")
        response1 = self.client.get(url1,
                                    HTTP_AUTHORIZATION=self.auth_header2, format="json")
        self.assertIn('True', str(response1.data))
