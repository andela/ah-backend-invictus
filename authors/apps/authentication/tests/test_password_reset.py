from django.urls import reverse
from rest_framework import status
from authors.apps.authentication.models import User
from authors.apps.authentication.serializers import UserSerializer
from .reset_password_base import BaseTestCase


class UserSignUpTestCase(BaseTestCase):
    """
    Class Test Case for testing password reset 
    """

    fixtures = ['authors/apps/authentication/fixtures/pass_reset.json']

    def test_request_password_rest(self):
        """
        test a request to reset password
        """

        url = reverse('password_reset')
        response = self.client.post(url, self.reset_email_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Check your email address for a reset  link.')

    def test_post_new_password(self):
        """
        test a post new password to reset
        """

        url = reverse('password_reset_token', kwargs={'token':'mytokengoeshere'})
        response = self.client.post(url, self.reset_new_passwords_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Password reset successfull.')
