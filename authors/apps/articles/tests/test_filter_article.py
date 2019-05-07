# Django and Rest framework imports
from django.urls import reverse
from rest_framework import status
# Local imports
from .base import BaseTestCase


class TestSearchAirticle(BaseTestCase):
    """ class to tests filter artile functions"""

    def test_search_article_by_author_username(self):
        url = reverse('articles-list-create')
        url_list = reverse('list_articles')
        response = self.client.post(
            url, self.create_article_data, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(
            url_list + '?author=' + 'test1',
            HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_article_by_title(self):
        url = reverse('articles-list-create')
        url_list = reverse('list_articles')
        response = self.client.post(
            url, self.create_article_data,
            HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(
            url_list + '?title=' + 'Fresh kid wonders on stage at lugogo',
            HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_article_by_tag(self):
        url = reverse('articles-list-create')
        url_list = reverse('list_articles')
        response = self.client.post(
            url, self.create_article_data,
            HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(
            url_list + '?tag=' + 'edna',
            HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_article_by_tag_when_unauthenticated(self):
        url = reverse('articles-list-create')
        url_list = reverse('list_articles')
        response = self.client.post(
            url, self.create_article_data,
            HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(
            url_list + '?tag=' + 'edna', format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_article_by_title_when_unauthenticated(self):
        url = reverse('articles-list-create')
        url_list = reverse('list_articles')
        response = self.client.post(
            url, self.create_article_data,
            HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(
            url_list + '?title=' + 'Fresh kid wonders on stage at lugogo',
            format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
