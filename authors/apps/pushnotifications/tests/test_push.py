from django.urls import reverse

from rest_framework import status

from authors.apps.pushnotifications.models import PushNotification
from .base import BaseTestCase


class PushNotificationsTest(BaseTestCase):
    """
    Class Test Case for Testing push notifications functionality
    """

    def test_modelrepresentation_notification(self):
        """
        Method tests gor string model rep of message
        """
        self.assertTrue(self.pushnotification.message, str(self.pushnotification))
        
    def test_favorite_article_notification(self):
        """
        Method tests the favoriting article notification is saved
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_data,
            HTTP_AUTHORIZATION=self.auth_header, format="json")
        article_id = response.data['article']['id']
        url = '/api/articles/{}/favorites/'.format(article_id)
        response = self.client.get(
            url, HTTP_AUTHORIZATION=self.auth_header2, format="json")
        self.assertEqual(PushNotification.objects.count(), 2)

    def test_liking_article_notification(self):
        """
        Method tests the liking article notification is saved
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_data,
            HTTP_AUTHORIZATION=self.auth_header, format="json")
        article_id = response.data['article']['id']
        url = '/api/articles/{}/like/'.format(article_id)
        response = self.client.post(
            url, HTTP_AUTHORIZATION=self.auth_header2, format="json")
        self.assertEqual(PushNotification.objects.count(), 2)

    def test_disliking_article_notification(self):
        """
        Method tests the disliking article notification is saved
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_data,
            HTTP_AUTHORIZATION=self.auth_header, format="json")
        article_id = response.data['article']['id']
        url = '/api/articles/{}/dislike/'.format(article_id)
        response = self.client.post(
            url, HTTP_AUTHORIZATION=self.auth_header2, format="json")
        self.assertEqual(PushNotification.objects.count(), 2)

    def test_commenting_article_notification(self):
        """
        Method tests the commenting article notification is saved
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_data,
            HTTP_AUTHORIZATION=self.auth_header, format="json")
        article_id = response.data['article']['id']
        url = '/api/articles/{}/comments/'.format(article_id)
        response = self.client.post(
            url, self.comment, HTTP_AUTHORIZATION=self.auth_header2,  format="json")
        self.assertEqual(PushNotification.objects.count(), 2)

    def test_following_user_notification(self):
        """
        Method tests the following user notification is saved
        """
        url = '/api/profiles/marcus/follow/'
        response = self.client.post(
            url, self.comment, HTTP_AUTHORIZATION=self.auth_header,  format="json")
        self.assertEqual(PushNotification.objects.count(), 2)
