# Django and Rest framework imports
from django.urls import reverse
from rest_framework import status
# Local imports
from .base import BaseTestCase
from django.contrib.auth import get_user_model


class UserLoginTestCase(BaseTestCase):
    """
    Class Test Case for Testing user Login functionality
    """

    def test_user_can_login(self):
        """
        Method tests the user login functionality
        """
        url = reverse('user_login')
        User = get_user_model()
        user = User.objects.get(email="sanyaken@gmail.com")
        setattr(user, 'email_verified', True)
        user.save()
        response = self.client.post(url, self.data.login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['token'])
        self.assertIsInstance(response.data['token'], str)
        self.assertEqual(response.data['email'], 'sanyaken@gmail.com')

    def test_returns_error_if_user_credentials_are_wrong_on_login(self):
        """
        Method tests if the API returns an error
        if a user provides wrong credentials on login
        """
        url = reverse('user_login')
        response = self.client.post(
            url, self.data.wrong_login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("A user with this email and password was not found.",
                      response.data['errors']['error'])

    def test_returns_error_if_user_provides_blank_email_on_login(self):
        """
        Method tests if the API returns an error
        if a user leaves email field blank on login
        """
        url = reverse('user_login')
        response = self.client.post(url, self.data.blank_email, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This field may not be blank.",
                      response.data['errors']['email'])

    def test_returns_error_if_user_provides_blank_password_on_login(self):
        """
        Method tests if the API returns an error
        if a user leaves password field blank on login
        """
        url = reverse('user_login')
        response = self.client.post(
            url, self.data.blank_password, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This field may not be blank.",
                      response.data['errors']['password'])

    def test_returns_error_if_user_provides_no_email_on_login(self):
            """
            Method tests if the API returns an error
            if a user leaves password field blank on login
            """
            url = reverse('user_login')
            response = self.client.post(
                url, self.data.no_email_on_login, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn("This field is required",
                        str(response.data['errors']['email']))
