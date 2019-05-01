from django.urls import reverse
from rest_framework import status
from .base import BaseTestCase


class FavoritesTestCase(BaseTestCase):
    """
    Class Test Case for testing favorites functionality
    """
    fixtures = ['authors/apps/favorites/fixtures/fixture.json']

    def test_adding_an_existing_favorite(self):
        """test marking an aticle as favorite"""
        url = reverse('favorite', kwargs={'article_id': 1})
        response = self.client.get(url,
            HTTP_AUTHORIZATION=self.joel_auth_header, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'],
            'Article removed from favorites.')

    def test_adding_favorite(self):
        """test marking an aticle as favorite"""
        url = reverse('favorite', kwargs={'article_id': 2})
        response = self.client.get(url,
            HTTP_AUTHORIZATION=self.joel_auth_header, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['message'],
            "Article added to favorites.")

    def test_favoriting_a_none_existing_article(self):
        """ test marking an absent aticle as favorite"""
        url = reverse('favorite', kwargs={'article_id': 341})
        response = self.client.get(url,
            HTTP_AUTHORIZATION=self.joel_auth_header, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_favoriting_your_own_article(self):
        """ test favoriting a self owned aticle"""
        url = reverse('favorite', kwargs={'article_id': 1})
        response = self.client.get(url,
            HTTP_AUTHORIZATION=self.sanya_auth_header, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'],
            'You can not favorite your own article!')

    def test_getting_favorite_articles(self):
        """ test getting favorite aticles """
        url = reverse('favorites')
        response = self.client.get(url,
            HTTP_AUTHORIZATION=self.joel_auth_header,
            format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_getting_empty_favorites(self):
        """ test getting empty favorite aticles """
        url = reverse('favorites')
        response = self.client.get(url,
            HTTP_AUTHORIZATION=self.sanya_auth_header,
            format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
