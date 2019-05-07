from django.urls import reverse

from rest_framework import status

from .base import BaseTestCase


class CommentTestCase(BaseTestCase):
    """
    Testcases for the comment API views.
    """

    def test_comment_model_returns_string_object(self):
        """Test comment object string representation is returned."""
        self.assertTrue(self.comment_data.body, str(self.comment_data))

    def test_get_comment_list(self):
        """Test get comment list."""
        url = reverse('comment_list', kwargs={'article_id': 1})
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_comment_list_article_not_found(self):
        """Test get comment list on article not found."""
        url = reverse('comment_list', kwargs={'article_id': 1000})
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()['error'], 'Article not found.')

    def test_get_comment_list_unauthorized_user(self):
        """Test get comment list for an unauthorized user."""
        url = reverse('comment_list', kwargs={'article_id': 1000})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_a_comment(self):
        """Test post a comment on an article."""
        url = reverse('comment_list', kwargs={'article_id': 1})
        response = self.client.post(url, self.comment,
                                    HTTP_AUTHORIZATION=self.auth_header,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_a_comment_article_not_found(self):
        """Test post a comment on article not found."""
        url = reverse('comment_list', kwargs={'article_id': 1000})
        response = self.client.post(url, self.comment,
                                    HTTP_AUTHORIZATION=self.auth_header,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_a_comment(self):
        """Test get a single comment."""
        # post an article
        url = reverse('comment_list', kwargs={'article_id': 1})
        self.client.post(url, self.comment,
                         HTTP_AUTHORIZATION=self.auth_header, format="json")
        # get a single article
        url = reverse('comment_detail', kwargs={'article_id': 1, 'pk': 1})
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_a_comment_on_article_not_found(self):
        """Test get a single comment on a non existinng article."""
        # post an article
        url = reverse('comment_list', kwargs={'article_id': 1})
        self.client.post(url, self.comment,
                         HTTP_AUTHORIZATION=self.auth_header, format="json")
        # get a single article
        url = reverse('comment_detail', kwargs={'article_id': 1000, 'pk': 1})
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()['error'], 'Article not found.')

    def test_get_a_comment_not_found(self):
        """Test get a single comment on a non existinng article."""
        # post an article
        post_url = reverse('comment_list', kwargs={'article_id': 1})
        self.client.post(post_url, self.comment,
                         HTTP_AUTHORIZATION=self.auth_header, format="json")
        # get a single comment
        url = reverse('comment_detail', kwargs={'article_id': 1, 'pk': 1000})
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()['error'], 'Comment not found.')

    def test_update_a_comment(self):
        """Test update a single comment."""
        # post an article
        post_url = reverse('comment_list', kwargs={'article_id': 1})
        response = self.client.post(post_url, self.comment,
                         HTTP_AUTHORIZATION=self.auth_header, format="json")
        comment_id = response.data['comment']['id']
        # update a comment
        url = reverse('comment_detail', kwargs={'article_id': 1, 'pk': comment_id})
        response = self.client.put(url, self.comment2,
                                   HTTP_AUTHORIZATION=self.auth_header,
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'],
                         'Comment successfully updated.')

    def test_update_a_comment_on_article_not_found(self):
        """Test update a single comment for a non existing article."""
        # post an article
        post_url = reverse('comment_list', kwargs={'article_id': 1})
        self.client.post(post_url, self.comment,
                         HTTP_AUTHORIZATION=self.auth_header, format="json")
        # update a comment
        url = reverse('comment_detail', kwargs={'article_id': 1000, 'pk': 5})
        response = self.client.put(url, self.comment2,
                                   HTTP_AUTHORIZATION=self.auth_header,
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()['error'], 'Article not found.')

    def test_update_a_comment_on_user_unauthorized(self):
        """Test update a single comment for an unauthorized user."""
        # post an article
        post_url = reverse('comment_list', kwargs={'article_id': 1})
        response = self.client.post(post_url, self.comment,
                         HTTP_AUTHORIZATION=self.auth_header,
                         format="json")
        comment_id = response.data['comment']['id']
        # login another user
        login_url = reverse('user_login')
        response = self.client.post(login_url, self.data2, format="json")
        token = response.data['token']
        auth_header = 'Bearer {}'.format(token)
        # update a comment
        url = reverse('comment_detail', kwargs={'article_id': 1, 'pk': comment_id})
        comment2 = {
            "comment": {
                "body": "His name was my name too..."
            }
        }
        response = self.client.put(url, comment2,
                                   HTTP_AUTHORIZATION=auth_header,
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json()['error'],
                         'You do not have permissions to edit this comment.')

    def test_owner_delete_a_comment(self):
        """Test delete a single comment."""
        url = reverse('comment_list', kwargs={'article_id': 1})
        response = self.client.post(url, self.comment3,
                         HTTP_AUTHORIZATION=self.auth_header,
                         format="json")
        comment_id = response.data['comment']['id']
        url = reverse('comment_detail', kwargs={'article_id': 1, 'pk': comment_id})
        response = self.client.delete(url, HTTP_AUTHORIZATION=self.auth_header,
                                      format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_owner_delete_a_comment_article_not_found(self):
        """Test delete a single comment article not found."""
        url = reverse('comment_list', kwargs={'article_id': 1})
        response = self.client.post(url, self.comment3,
                                    HTTP_AUTHORIZATION=self.auth_header,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        comment_id = response.data['comment']['id']
        url = reverse('comment_detail', kwargs={'article_id': 1000, 'pk': comment_id})
        response = self.client.delete(url, HTTP_AUTHORIZATION=self.auth_header,
                                      format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthorized_user_delete_comment(self):
        """Test update a single comment for an unauthorized user."""
        # post an article
        post_url = reverse('comment_list', kwargs={'article_id': 1})
        response = self.client.post(post_url, self.comment,
                         HTTP_AUTHORIZATION=self.auth_header,
                         format="json")
        comment_id = response.data['comment']['id']
        # login another user
        login_url = reverse('user_login')
        response = self.client.post(login_url, self.data2, format="json")
        token = response.data['token']
        auth_header = 'Bearer {}'.format(token)
        # delete a comment
        url = reverse('comment_detail', kwargs={'article_id': 1, 'pk': comment_id})
        response = self.client.delete(url, HTTP_AUTHORIZATION=auth_header,
                                      format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
