from django.urls import reverse

from rest_framework import status

from .base import BaseTestCase


class CommentEditHistoryTestCase(BaseTestCase):
    """
    Testcases for the comment edit hostory API view.
    """

    def test_get_comment_update_history(self):
        """Test get comment update history."""
        post_url = reverse('comment_list', kwargs={'article_id': 1})
        post = self.client.post(post_url, self.comment,
                                HTTP_AUTHORIZATION=self.auth_header,
                                format="json")
        comment_id = post.data['comment']['id']
        update_url = reverse('comment_detail',
                             kwargs={'article_id': 1, 'pk': comment_id})
        response = self.client.put(update_url, self.comment2,
                                   HTTP_AUTHORIZATION=self.auth_header,
                                   format="json")
        history_url = reverse('update_history',
                              kwargs={'article_id': 1, 'pk': comment_id})
        response = self.client.get(history_url,
                                   HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_comment_update_history_no_article(self):
        """Test get comment update history on a non existing article."""
        post_url = reverse('comment_list', kwargs={'article_id': 1})
        post = self.client.post(post_url, self.comment,
                                HTTP_AUTHORIZATION=self.auth_header,
                                format="json")
        comment_id = post.data['comment']['id']
        update_url = reverse('comment_detail',
                             kwargs={'article_id': 1, 'pk': comment_id})
        response = self.client.put(update_url, self.comment2,
                                   HTTP_AUTHORIZATION=self.auth_header,
                                   format="json")
        history_url = reverse('update_history',
                              kwargs={'article_id': 1000, 'pk': comment_id})
        response = self.client.get(history_url,
                                   HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()['error'], 'Article not found.')

    def test_get_comment_update_history_no_comment(self):
        """Test get comment update history on a non existing comment."""
        post_url = reverse('comment_list', kwargs={'article_id': 1})
        post = self.client.post(post_url, self.comment,
                                HTTP_AUTHORIZATION=self.auth_header,
                                format="json")
        comment_id = post.data['comment']['id']
        update_url = reverse('comment_detail',
                             kwargs={'article_id': 1, 'pk': comment_id})
        response = self.client.put(update_url, self.comment2,
                                   HTTP_AUTHORIZATION=self.auth_header,
                                   format="json")
        history_url = reverse('update_history',
                              kwargs={'article_id': 1, 'pk': 1000})
        response = self.client.get(history_url,
                                   HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()['error'], 'Comment not found.')
