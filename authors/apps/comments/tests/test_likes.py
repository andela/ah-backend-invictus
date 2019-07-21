from authors.apps.comments.tests.base import BaseTestCase
from django.urls import reverse


class TestLikeCommment(BaseTestCase):
    """Class to test like and unlike a comment."""

    def test_user_to_like_own_comment(self):
        """Test post a comment on an article and like a comment."""
        url = reverse('comment_list', kwargs={'article_id': 1})
        response = self.client.post(url, self.comment,
                                    HTTP_AUTHORIZATION=self.auth_header,
                                    format="json")
        comment_id = response.data['comment']['id']
        url1 = reverse('like_comment',
                       kwargs={'article_id': 1, 'pk': comment_id})
        response1 = self.client.post(url1, HTTP_AUTHORIZATION=self.auth_header,
                                     format="json")
        self.assertEqual(response1.status_code, 403)

    def test_user_liking_your_own_comment(self):
        """Test liking your own comment."""
        url = reverse('comment_list', kwargs={'article_id': 1})
        response = self.client.post(url, self.comment,
                                    HTTP_AUTHORIZATION=self.auth_header,
                                    format="json")
        comment_id = response.data['comment']['id']
        url1 = reverse('like_comment',
                       kwargs={'article_id': 1, 'pk': comment_id})
        response1 = self.client.post(url1, HTTP_AUTHORIZATION=self.auth_header,
                                     format="json")
        self.assertEqual(response1.data['message'],
                         "You can not like your own comment.")

    def test_user_to_liking_another_comment(self):
        """Test liking your own comment."""
        url = reverse('comment_list', kwargs={'article_id': 1})
        response = self.client.post(url, self.comment,
                                    HTTP_AUTHORIZATION=self.auth_header,
                                    format="json")
        comment_id = response.data['comment']['id']
        url1 = reverse('like_comment',
                       kwargs={'article_id': 1, 'pk': comment_id})
        response1 = self.client.post(url1,
                                     HTTP_AUTHORIZATION=self.auth_header2,
                                     format="json")
        self.assertEqual(response1.status_code, 200)

    def test_user_to_like_another_comment(self):
        """Test liking another comment."""
        url = reverse('comment_list', kwargs={'article_id': 1})
        response = self.client.post(url, self.comment,
                                    HTTP_AUTHORIZATION=self.auth_header,
                                    format="json")
        comment_id = response.data['comment']['id']
        url1 = reverse('like_comment',
                       kwargs={'article_id': 1, 'pk': comment_id})
        response1 = self.client.post(url1,
                                     HTTP_AUTHORIZATION=self.auth_header2,
                                     format="json")
        self.assertEqual(response1.data['success'],
                         "You have successfully liked this comment.")
        self.assertEqual(response1.status_code, 200)

    def test_user_to_like_twice_a_comment(self):
        """Test liking your own comment."""
        url = reverse('comment_list', kwargs={'article_id': 1})
        response = self.client.post(url, self.comment,
                                    HTTP_AUTHORIZATION=self.auth_header,
                                    format="json")
        comment_id = response.data['comment']['id']
        url1 = reverse('like_comment',
                       kwargs={'article_id': 1, 'pk': comment_id})
        response1 = self.client.post(url1,
                                     HTTP_AUTHORIZATION=self.auth_header2,
                                     format="json")
        response1 = self.client.post(url1,
                                     HTTP_AUTHORIZATION=self.auth_header2,
                                     format="json")
        self.assertEqual(response1.data['message'],
                         "Your like has been cancelled")
        self.assertEqual(response1.status_code, 200)

    def test_user_has_liked_a_comment(self):
        """Test a user has ever liked a comment."""
        url = reverse('comment_list', kwargs={'article_id': 1})
        response = self.client.post(url, self.comment,
                                    HTTP_AUTHORIZATION=self.auth_header,
                                    format="json")
        comment_id = response.data['comment']['id']
        url1 = reverse('like_comment',
                       kwargs={'article_id': 1, 'pk': comment_id})
        self.client.post(url1, HTTP_AUTHORIZATION=self.auth_header2,
                         format="json")
        url1 = reverse('get_likes',
                       kwargs={'article_id': 1, 'pk': comment_id})
        response1 = self.client.get(url1,
                                    HTTP_AUTHORIZATION=self.auth_header2,
                                    format="json")
        self.assertEqual(response1.status_code, 200)
        self.assertIn('True', str(response1.data))

    def test_user_has_not_liked_a_comment(self):
        """Test a user has never liked a comment."""
        url = reverse('comment_list', kwargs={'article_id': 1})
        response = self.client.post(url, self.comment,
                                    HTTP_AUTHORIZATION=self.auth_header,
                                    format="json")
        comment_id = response.data['comment']['id']
        url1 = reverse('get_likes',
                       kwargs={'article_id': 1, 'pk': comment_id})
        response1 = self.client.get(url1,
                                    HTTP_AUTHORIZATION=self.auth_header2,
                                    format="json")
        self.assertEqual(response1.status_code, 200)
        self.assertIn('False', str(response1.data))
