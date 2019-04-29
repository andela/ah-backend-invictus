# Django and Rest framework imports
from django.urls import reverse
from rest_framework import status
# Local imports
from .base import BaseTestCase


class GetUsersTestCase(BaseTestCase):
    """"
    Test case for get user and update user endpoints
    """

    def test_gets_users(self):
        url = reverse('retrieveupdate')
        response = self.client.get(
            url, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'adminuser')
