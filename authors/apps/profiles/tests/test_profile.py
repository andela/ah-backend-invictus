from django.urls import reverse
from rest_framework import status
from .base import BaseTestCase


class ProfileTestCase(BaseTestCase):
    """Testcases for the user profile views."""


    def test_lastname_in_profile_returns_string(self):
        """method to test whether lastname is a string"""
        self.assertTrue(self.profile["profile"]["lastname"], str(self.profile))

    def test_get_userprofile(self):
        """Test get user profile."""
        url = reverse('update_profile', kwargs={'username': 'test1'})
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_profile_which_doesnot_exist(self):
        """Test get profile which doesnot exist."""
        url = reverse('update_profile', kwargs={'username': 'test200'})
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_profile_when_not_authorized(self):
        """Test user profile for unauthorized user."""
        url = reverse('update_profile', kwargs={'username': 'test200'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_a_user_profile(self):
        """Test update a profile."""
        url = reverse('update_profile', kwargs={'username': 'test1'})
        response = self.client.put(url, self.profile2,
                                    HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_profile_which_doenot_exist(self):
        """Test update profile which doesnot exist."""
        url = reverse('update_profile', kwargs={'username': 'test1234'})
        response = self.client.put(url, self.profile2,
                                   HTTP_AUTHORIZATION=self.auth_header,
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_profile_for_unauthorized_user(self):
        """Test update profile for an unauthorized user."""
        login_url = reverse('user_login')
        response = self.client.post(login_url, self.data2, format="json")
        token = response.data['token']
        auth_header = 'Bearer {}'.format(token)
        url = reverse('update_profile', kwargs={'username': 'test12345'})

        response = self.client.put(url, self.profile2, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_firstname_in_profile_returns_string(self):
        """method to test whether firstname is a string"""
        self.assertTrue(self.profile["profile"]["firstname"], str(self.profile))

    def test_bio_in_profile_returns_string(self):
        """method to test whether bio is a string"""
        self.assertTrue(self.profile["profile"]["bio"], str(self.profile))

    def test_image_in_profile_returns_string(self):
        """method to test whether bio is a string"""
        self.assertTrue(self.profile["profile"]["image"], str(self.profile))

    def test_update_profile_with_firstname_less_three(self):
        """method to test firstname is less than three characters"""
        url = reverse('update_profile', kwargs={'username': 'test1'})
        response = self.client.put(url, self.profile3,
                                   HTTP_AUTHORIZATION=self.auth_header,
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_profile_with_lastname_less_four(self):
        """method to test lastname is less than three characters"""
        url = reverse('update_profile', kwargs={'username': 'test1'})
        response = self.client.put(url, self.profile4,
                                   HTTP_AUTHORIZATION=self.auth_header,
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_profile_username_which_doesnot_exist(self):
        """method to test username is less than three characters"""
        url = reverse('update_profile', kwargs={'username': 'te'})
        response = self.client.put(url, self.profile5,
                                   HTTP_AUTHORIZATION=self.auth_header,
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

