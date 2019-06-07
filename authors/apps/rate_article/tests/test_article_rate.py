from rest_framework import status
from django.urls import reverse
from .test_base import BaseTestCase


class TestRateArticle(BaseTestCase):
    """class to test article rate"""

    fixtures = ['authors/apps/rate_article/fixtures/rate_article.json']

    def test_cannot_rate_own_article(self):
        """tests user cannot rate own article"""

        url = reverse('rating', kwargs={"article_id": 1})
        response = self.client.post(url,
                                    HTTP_AUTHORIZATION=self.edna_auth_header,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["error"],
                         "you cannot rate your own article")

    def test_rate_article_succesfully(self):
        """tests that article is succesfully rated"""
        url = reverse('rating', kwargs={"article_id": 1})
        response = self.client.post(url,
                                    HTTP_AUTHORIZATION=self.joel_auth_header1,
                                    data={"rating": 3},
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_rate_article_that_does_not_exist(self):
        """tests rate an article that does not exist"""
        url = reverse('rating', kwargs={"article_id": 4})
        response = self.client.get(url,
                                   HTTP_AUTHORIZATION=self.joel_auth_header1,
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_rate_article_with_negative_rating(self):
        """tests cannot rate with negative digit"""
        url = reverse('rating', kwargs={"article_id": 1})
        response = self.client.post(url,
                                    HTTP_AUTHORIZATION=self.joel_auth_header1,
                                    data={"rating": -1},
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["errors"]['rating'][0],
                         "rating should include numbers 1 to 5")

    def test_get_article_average(self):
        """tests getting article average"""
        url = reverse('rating', kwargs={"article_id": 1})
        response = self.client.get(url,
                                   HTTP_AUTHORIZATION=self.joel_auth_header1,
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_average_rating_that_doestnot_exist(self):
        """tests getting average of article that doesnot exist"""
        url = reverse('rating', kwargs={"article_id": 4})
        response = self.client.get(url,
                                   HTTP_AUTHORIZATION=self.joel_auth_header1,
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_rate_of_article(self):
        """test cannot rate more than once"""
        url = reverse('rating', kwargs={"article_id": 1})
        response = self.client.post(url,
                                    HTTP_AUTHORIZATION=self.joel_auth_header1,
                                    data={"rating": 3},
                                    format="json")
        response = self.client.post(url,
                                    HTTP_AUTHORIZATION=self.joel_auth_header1,
                                    data={"rating": 3},
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
