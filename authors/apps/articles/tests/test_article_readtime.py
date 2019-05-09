from django.urls import reverse
from .base import BaseTestCase
from .readtime_test_data import less_than_a_minute, one_hour_read,\
    days_read, minutes_read


class ArticleReadTimeTestCase(BaseTestCase):
    """
    Class for testing the article read time
    """

    def test_api_estimates_articles_of_less_than_a_minute(self):
        """
        Method tests if the api returns readtime of less then a minute
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, less_than_a_minute, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data["article"]["read_time"], "less than a minute read")

    def test_api_estimates_minute_long_article_read_time(self):
        """
        Method tests if the api returns readtime in minutes if the article
        takes minutes to read
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, minutes_read, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("minute read", str(response.data))

    def test_api_estimates_hours_long_article_read_time(self):
        """
        Method tests if the api returns readtime in hours if the article
        takes hours to read
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, one_hour_read, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("hour read", str(response.data))

    def test_api_estimates_days_long_article_read_time(self):
        """
        Method tests if api returns readtime in days if the article 
        takes days to read
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, days_read, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("day read", str(response.data))
