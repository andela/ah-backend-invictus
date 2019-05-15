from django.urls import reverse
from rest_framework import status
# Local imports
from .base import BaseTestCase


class UserReadStatsTestCase(BaseTestCase):
    """
    class for testing user read statistics
    """

    def test_gets_user_read_statistics(self):
        stats_url = reverse('reading_stats')
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_data, HTTP_AUTHORIZATION=self.auth_header, format="json")
        response = self.client.get(
            stats_url, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['reading_statistics'][0]['article_id'], 36)
        self.assertEqual(response.data['reading_statistics'][0]['total_views'], 0)
        self.assertEqual(response.data['reading_statistics'][0]['total_reads'], 0)
        self.assertEqual(response.data['reading_statistics'][0]['read_ratio'], 0)
        self.assertEqual(response.data['reading_statistics'][0]['views_in_last_30_days'], 0)
        self.assertEqual(response.data['reading_statistics'][0]['reads_in_last_30_days'], 0)
        self.assertEqual(response.data['reading_statistics'][0]['likes_in_last_30_days'], 0)
        self.assertEqual(response.data['reading_statistics'][0]['dislikes_in_last_30_days'], 0)
