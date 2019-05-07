from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from django.urls import reverse
from unittest.mock import patch


class SocialAuthenticationTestcase(APITestCase):
    """Social Authentication Testcase."""

    def setUp(self):
        self.client = APIClient()
        self.facebook_correct_token = {
            "access_token": "correct_access_token"
        }
        self.facebook_wrong_token = {
            "access_token": "wrong_access_token"
        }
        self.google_token = {
            "access_token": "google_auth_token"
        }
        self.twitter_token = {
            "access_token": "access_token",
            "access_token_secret": "access_token_secret"
        }
        self.facebook_url = reverse("facebook_auth")
        self.google_url = reverse("google_auth")
        self.twitter_url = reverse("twitter_auth")

    @patch('facebook.GraphAPI.get_object')
    def test_facebook_authentication_create(self, get_object):
        """Test create a user with facebook authentication."""
        get_object.return_value = dict(
            email="example@example.com", name="example")
        response = self.client.post(self.facebook_url,
                                    self.facebook_correct_token, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch('facebook.GraphAPI.get_object')
    def test_facebook_authentication_login(self, get_object):
        """Test user login with facebook authentication."""
        get_object.return_value = dict(
            email="example@example.com", name="example")
        self.client.post(self.facebook_url, self.facebook_correct_token,
                         format="json")
        response = self.client.post(self.facebook_url,
                                    self.facebook_correct_token, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('facebook.GraphAPI', side_effect=Exception())
    def test_facebook_authentication_login_with_wrong_token(self, GraphAPI):
        """Test user login with wrong facebook authentication token."""
        self.client.post(self.facebook_url, self.facebook_correct_token,
                         format="json")
        response = self.client.post(self.facebook_url,
                                    self.facebook_wrong_token, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('google.oauth2.id_token.verify_oauth2_token')
    def test_google_authentication_create(self, verify_oauth2_token):
        """Test create user with google authentication."""
        verify_oauth2_token.return_value = dict(
            email="example@example.com", name="example")
        response = self.client.post(self.google_url, self.google_token,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch('google.oauth2.id_token.verify_oauth2_token')
    def test_google_authentication_user_login(self, verify_oauth2_token):
        """Test user login with google authentication."""
        verify_oauth2_token.return_value = dict(
            email="example@example.com", name="example")
        self.client.post(self.google_url, self.google_token, format="json")
        response = self.client.post(self.google_url, self.google_token,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('google.oauth2.id_token.verify_oauth2_token',
           side_effect=Exception())
    def test_google_authentication_with_wrong_token(self, verify_oauth2_token):
        """Test user login with wrong google authentication token."""
        response = self.client.post(self.google_url, self.google_token,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('twitter.Api.VerifyCredentials')
    def test_twitter_authentication_create(self, VerifyCredentials):
        """Test create user with twitter authentication."""
        VerifyCredentials.return_value.__dict__ = dict(
            email="example@example.com", name="example")
        response = self.client.post(self.twitter_url, self.twitter_token,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch('twitter.Api.VerifyCredentials')
    def test_twitter_authentication_user_login(self, VerifyCredentials):
        """Test user login with twitter social authentication."""
        VerifyCredentials.return_value.__dict__ = dict(
            email="example@example.com", name="example")
        self.client.post(self.twitter_url, self.twitter_token, format="json")
        response = self.client.post(self.twitter_url, self.twitter_token,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('twitter.Api.VerifyCredentials', side_effect=Exception)
    def test_twitter_authentication_with_wrong_token(self, VerifyCredentials):
        """Test user login with wrong twitter authentication token."""
        response = self.client.post(self.twitter_url, self.twitter_token,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
