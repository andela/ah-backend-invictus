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
        self.assertEqual(response.data['message'], 'Check your email-address for a reset-password link.')

    def test_post_new_password(self):
        """
        test a post new password to reset
        """
        url = reverse('password_reset_token', kwargs={'token':'mytokengoeshere'})
        response = self.client.post(url, self.reset_new_passwords_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Password reset was successfull.')

    def test_reset_wrong_token(self):
        """
        test a post new password to reset
        """
        url = reverse('password_reset_token', kwargs={'token':'ytokengoeshere'})
        response = self.client.post(url, self.reset_new_passwords_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['message'], 'Ivalid token!')

    def test_post_wrong_new_password(self):
        """
        test post an invalid new password to reset
        """
        url = reverse('password_reset_token', kwargs={'token':'mytokengoeshere'})
        response = self.client.post(url, self.reset_invalid_new_passwords_data)
        error_message = {
                    "password": [
                        "Password should include numbers and alphabets and one special character"
                    ]
            }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'], error_message)

    def test_post_same_password(self):
        """
        test post an invalid new password to reset
        """
        url = reverse('password_reset_token', kwargs={'token':'mytokengoeshere'})
        response = self.client.post(url, self.reset_same_password_data)
        error_message = "New password should be different from previous password."
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], error_message)
