from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from rest_framework import status
from rest_framework .test import APITestCase, APIClient

from .user_data import UserTestData


class UserManagerTestCase(APITestCase):
    """Usermanager TestCase."""

    def setUp(self):
        User = get_user_model()
        self.client = APIClient()
        self.user_test_data = UserTestData()
        self.user = User.objects.create_user(
            username='test1', email='test1@example.com', password='12345678'
        )

    def test_create_user(self):
        """Test create user."""
        self.assertEqual(self.user.username, 'test1')
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_user_model_returns_string_object(self):
        """Test user object string representation is returned."""
        self.assertTrue(self.user.username, str(self.user))

    def test_return_full_name(self):
        """Test return get full name."""
        self.assertTrue(self.user.get_full_name)

    def test_return_short_name(self):
        """Test return get short name."""
        self.assertEqual(self.user.get_short_name(), 'test1')

    def test_create_user_with_no_username(self):
        """Test create user with no username."""
        User = get_user_model()
        with self.assertRaisesMessage(TypeError,
                                      'Users must have a username.'):
            User.objects.create_user(
                username=None, email='test1@example.com', password='12345678'
            )

    def test_create_user_with_no_email(self):
        """Test create user with no email."""
        User = get_user_model()
        with self.assertRaisesMessage(TypeError,
                                      'Users must have an email address.'):
            User.objects.create_user(
                username='test1', email=None, password='12345678'
            )

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

    def test_create_superuser_with_no_password(self):
        """Test create superuser with no password."""
        User = get_user_model()
        with self.assertRaisesMessage(TypeError,
                                      'Superusers must have a password.'):
            User.objects.create_superuser(
                username='admin2', email='admin2@example.com', password=None
            )

    def test_user_signup(self):
        """Test user signup."""
        url = reverse('authentication:user_signup')
        response = self.client.post(url, self.user_test_data.user_registration,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        """Test user login."""
        registration_url = reverse('authentication:user_signup')
        login_url = reverse('authentication:user_login')
        self.client.post(registration_url,
                         self.user_test_data.user_registration, format="json")
        User = get_user_model()
        user = User.objects.get(
            email=self.user_test_data.user_registration['user']['email'])
        setattr(user, 'email_verified', True)
        user.save()
        response = self.client.post(login_url, self.user_test_data.user_login,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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
        activation_url = reverse('authentication:activation_link',
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
        activation_url = reverse('authentication:activation_link',
                                 kwargs=kwargs)
        response = self.client.get(activation_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(user3, None)

    def test_activation_link_user_not_found(self):
        """Test user registration activation link is invalid."""
        User = get_user_model()
        user3 = User.objects.create_user(
            username='test3', email='test3@example.com', password='12345678'
        )
        uid = user3.id
        kwargs = {
            "uid": urlsafe_base64_encode(force_bytes(uid)).decode('utf-8')
        }
        activation_url = reverse('authentication:activation_link',
                                 kwargs=kwargs)
        response = self.client.get(activation_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
