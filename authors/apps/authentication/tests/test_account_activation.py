# Django and restframework imports
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework import status
# Local imports
from .base import BaseTestCase


class UserVerificationTestCase(BaseTestCase):
    """User Verification TestCase."""
    def test_create_user(self):
        """Test create user."""
        self.assertEqual(self.user.username, 'test1')
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_return_full_name(self):
        """Test return get full name."""
        self.assertTrue(self.user.get_full_name)

    def test_return_short_name(self):
        """Test return get short name."""
        self.assertEqual(self.user.get_short_name(), 'test1')

    def test_create_superuser(self):
        """Test create superuser."""
        User = get_user_model()
        user = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='12345678'
        )
        self.assertEqual(user.username, 'admin')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_activation_link(self):
        """Test user can get activation link to activate account."""
        User = get_user_model()
        user2 = User.objects.create_user(
            username='test3', email='test3@example.com', password='12345678'
        )
        uid = user2.username
        kwargs = {
            "uid": urlsafe_base64_encode(force_bytes(uid)).decode('utf-8')
        }
        activation_url = reverse('activation_link',
                                 kwargs=kwargs)
        response = self.client.get(activation_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_activation_link_invalid(self):
        """Test user registration activation link is invalid."""
        User = get_user_model()
        user3 = User.objects.create_user(
            username='test3', email='test3@example.com', password='12345678'
        )
        uid = user3.id
        kwargs = {
            "uid": urlsafe_base64_encode(force_bytes(uid)).decode('utf-8')
        }
        activation_url = reverse('activation_link',
                                 kwargs=kwargs)
        response = self.client.get(activation_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(user3)

    def test_activation_link_user_not_found(self):
        """
        Method returns an error if the user is not found 
        when they attempt to activate an account
        """
        User = get_user_model()
        user3 = User.objects.create_user(
            username='test3', email='test3@example.com', password='12345678'
        )
        uid = user3.id
        kwargs = {
            "uid": urlsafe_base64_encode(force_bytes(uid)).decode('utf-8')
        }
        activation_url = reverse('activation_link',
                                 kwargs=kwargs)
        response = self.client.get(activation_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
