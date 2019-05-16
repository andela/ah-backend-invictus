from django.urls import reverse

from rest_framework import status

from .base import BaseTestCase
from authors.apps.authentication.models import User


class ReportTest(BaseTestCase):
    """
    Class Test Case for Testing reporting functionality
    """

    def test_user_report_article_status(self):
        """
        Method tests the status on report article response
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_data, HTTP_AUTHORIZATION=self.auth_header, format="json")
        article_id = response.data['article']['id']
        url = '/api/articles/{}/report/'.format(article_id)
        response = self.client.post(
            url, self.report, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_report_missing_article(self):
        """
        Method tests the status on reporting a missing article
        """
        url = '/api/articles/0/report/'
        response = self.client.post(
            url, self.report, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_report_article_message(self):
        """
        Method tests the message when a report is successfull
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_data, HTTP_AUTHORIZATION=self.auth_header, format="json")
        article_id = response.data['article']['id']
        url = '/api/articles/{}/report/'.format(article_id)
        response = self.client.post(
            url, self.report, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.data['message'],
                         "Report successfully created.")

    def test_user_report_article_twice_message(self):
        """
        Method tests the message when the same user reports an article twice
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_data, HTTP_AUTHORIZATION=self.auth_header, format="json")
        article_id = response.data['article']['id']
        url = '/api/articles/{}/report/'.format(article_id)
        response = self.client.post(
            url, self.report, HTTP_AUTHORIZATION=self.auth_header, format="json")
        response = self.client.post(
            url, self.report, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.data['error'],
                         "You already reported this article")

    def test_user_report_article_blank_reason(self):
        """
        Method tests the message when a reason is blank
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_data, HTTP_AUTHORIZATION=self.auth_header, format="json")
        article_id = response.data['article']['id']
        url = '/api/articles/{}/report/'.format(article_id)
        response = self.client.post(
            url, self.report_with_blank_reason, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_report_article_no_reason(self):
        """
        Method tests the message when there is no reason in request body
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_data, HTTP_AUTHORIZATION=self.auth_header, format="json")
        article_id = response.data['article']['id']
        url = '/api/articles/{}/report/'.format(article_id)
        response = self.client.post(
            url, self.report_with_no_reason, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_without_permisions_view_report(self):
        """
        Method tests whether a non admin user can view all reports endpoint
        """
        url = '/api/articles/reports/'
        response = self.client.get(
            url, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_without_permisions_view_report_message(self):
        """
        Method tests message when a non admin user can view all reports endpoint
        """
        url = '/api/articles/reports/'
        response = self.client.get(
            url, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(
            response.data['error'], "You do not have permission to view the reported articles")

    def test_user_with_permisions_view_report_status(self):
        """
        Method tests status when a admin user can view all reports endpoint
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_data, HTTP_AUTHORIZATION=self.auth_header, format="json")
        article_id = response.data['article']['id']
        url = '/api/articles/{}/report/'.format(article_id)
        response = self.client.post(
            url, self.report, HTTP_AUTHORIZATION=self.auth_header, format="json")
        url = '/api/articles/reports/'
        response = self.client.get(
            url, HTTP_AUTHORIZATION=self.super_auth_header, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_200_OK)

    def test_user_with_permisions_view_report_message(self):
        """
        Method tests status when a admin user can view all reports endpoint
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_data, HTTP_AUTHORIZATION=self.auth_header, format="json")
        article_id = response.data['article']['id']
        url = '/api/articles/{}/report/'.format(article_id)
        response = self.client.post(
            url, self.report, HTTP_AUTHORIZATION=self.auth_header, format="json")
        url = '/api/articles/reports/'
        response = self.client.get(
            url, HTTP_AUTHORIZATION=self.super_auth_header, format="json")
        self.assertIn(
            "report", str(response.data))
