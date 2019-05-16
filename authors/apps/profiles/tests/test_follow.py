from django.urls import reverse
from rest_framework import status
from .base import BaseTestCase


class FollowTestCase(BaseTestCase):
    """Testcases for following a user."""

    def test_follow_user_post(self):
        """Test start following a user."""
        url = reverse('follow', kwargs={'username': 'test2'})
        response = self.client.post(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_follow_your_self(self):
        """Test start following self."""
        url = reverse('follow', kwargs={'username': 'test1'})
        response = self.client.post(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_follow_already_followed_user(self):
        """Test start following a user you already follow."""
        url = reverse('follow', kwargs={'username': 'test2'})
        self.client.post(url, HTTP_AUTHORIZATION=self.auth_header)
        response = self.client.post(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_follow_missing_user_post(self):
        """Test trying to start following a missing user."""
        url = reverse('follow', kwargs={'username': 'joel'})
        response = self.client.post(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_follow(self):
        """Test unfollowing a user"""
        url = reverse('follow', kwargs={'username': 'test2'})
        self.client.post(url, HTTP_AUTHORIZATION=self.auth_header)
        response = self.client.delete(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_follow_of_not_followed_user(self):
        """Test unfollowing a user you are not following"""
        url = reverse('follow', kwargs={'username': 'test2'})
        response = self.client.delete(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_followers_of_user(self):
        """Test list followers of a user"""
        url_followers = reverse('getfollowers', kwargs={'username': 'test2'})
        self.client.get(url_followers, HTTP_AUTHORIZATION=self.auth_header)
        url_follow = reverse('follow', kwargs={'username': 'test2'})
        self.client.post(url_follow, HTTP_AUTHORIZATION=self.auth_header)
        response = self.client.get(url_followers, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_user_is_following(self):
        """Test list users the user is following"""
        url_following = reverse('getfollowing', kwargs={'username': 'test1'})
        self.client.get(url_following, HTTP_AUTHORIZATION=self.auth_header)
        url_follow = reverse('follow', kwargs={'username': 'test2'})
        self.client.post(url_follow, HTTP_AUTHORIZATION=self.auth_header)
        response = self.client.get(url_following, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
