# Django and restframework imports
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
# Local imports
from authors.apps.authentication.models import User
from .base import BaseTestCase


class UserSignUpTestCase(BaseTestCase):
    """
    Class Test Case for testing user signup 
    functionality
    Class also tests the user model
    """

    def test_user_model(self):
        """
        Method tests the user model for the API
        """
        user = User(
            email=self.data.signup_data['user']['email'],
            username=self.data.signup_data['user']['username'],
            password=self.data.signup_data['user']['password']
        )
        self.assertEqual(user.username, 'sanyat')
        self.assertEqual(user.email, 'sanyakennetht@gmail.com')

    def test_user_model_returns_error_if_no_email_is_provided(self):
        """
        Method tests the user model for the API
        """
        User = get_user_model()
        with self.assertRaises(TypeError):
            self.user = User.objects.create_user( email=None,
            username=self.data.signup_data['user']['username'], password='12345678'
            )

    def test_user_model_returns_error_if_no_username_is_provided(self):
        """
        Method tests the user model for the API
        """
        User = get_user_model()
        with self.assertRaises(TypeError):
            self.user = User.objects.create_user( email=self.data.signup_data['user']['username'],
            username=None, password='12345678'
            )
    
    def test_user_model_returns_error_if_no_password_is_provided_on_create_super_user(self):
        """
        Method tests the user model for the API
        """
        User = get_user_model()
        with self.assertRaises(TypeError):
            self.user = User.objects.create_superuser( email=self.data.signup_data['user']['email'],
            username=self.data.signup_data['user']['username'], password=None
            )

    def test_can_sign_up_user(self):
        """
        Method tests if the user can successfuly signup 
        """
        url = reverse('user_signup')
        response = self.client.post(url, self.data.signup_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'sanyat')

    def test_returns_error_if_username_is_blank_on_signup(self):
        url = reverse('user_signup')
        response = self.client.post(
            url, self.data.blank_username_on_signup, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This field may not be blank",
                      response.data['errors']['username'][0])
    
    def test_returns_error_if_useremail_is_blank_on_signup(self):
        url = reverse('user_signup')
        response = self.client.post(
            url, self.data.blank_email_on_signup, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This field may not be blank",
                      response.data['errors']['email'][0])
    
    def test_returns_error_if_password_is_blank_on_signup(self):
        url = reverse('user_signup')
        response = self.client.post(
            url, self.data.blank_password_on_signup, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Password field cannot be empty",
                      response.data['errors']['password'][0])

    def test_returns_error_if_password_is_short(self):
        url = reverse('user_signup')
        response = self.client.post(
            url, self.data.invalid_password_length, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Password should atleast be 8 characters.",
                      response.data['errors']['password'][0])

    def test_returns_error_if_email_is_invalid(self):
        url = reverse('user_signup')
        response = self.client.post(
            url, self.data.invalid_email_on_signup, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Enter a valid email address",
                      response.data['errors']['email'][0])

    def test_register_invalid_username(self):
        """test fail when username is invalid"""
        url = reverse('user_signup')
        response = self.client.post(url, self.data.invalid_username, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors']['username'][0], 'username should be longer than 4 characters')
    
    def test_register_username_with_spaces(self):
        """test fail when username has spaces is invalid"""
        url = reverse('user_signup')
        response = self.client.post(url, self.data.username_with_space, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors']['username']
                         [0], 'username should not contain spaces')

    def test_register_invalid_password(self):
        """test fail when password is invalid"""
        url = reverse('user_signup')
        response = self.client.post(url, self.data.invalid_password, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors']['password']
                         [0], 'Password should atleast be 8 characters.')

    def test_register_non_alphanumeric_password(self):
        """test fail when password is not alphanumeric"""
        url = reverse('user_signup')
        response = self.client.post(url, self.data.non_numeric_password, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors']['password'][0],
                         'Password should include numbers and alphabets and one special character')

    def test_register_password_with_whitespace(self):
        """test fail when password has spaces"""
        url = reverse('user_signup')
        response = self.client.post(url, self.data.password_with_space, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors']['password'][0],
                         'Password should not include white spaces')
    
    def test_user_exists(self):
        """Test register with email that exists """
        url = reverse('user_signup')
        response = self.client.post(url, self.data.signup_data, format="json")
        response = self.client.post(url, self.data.signup_data ,format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_username_with_no_characters(self):
        """Test username with no characters """
        url = reverse('user_signup')
        response = self.client.post(url, self.data.username_with_no_characters, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors']['username'][0],
                         'username should contain characters')
