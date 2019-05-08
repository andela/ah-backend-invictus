from django.urls import reverse
from .base import BaseTestCase


class BookmarkTestCase(BaseTestCase):
    """
    Class Test Case for bookmarks
    """
    def test_api_creates_user_bookmark_for_an_article(self):
        url = '/api/articles/1/bookmarks/'
        response = self.client.post(url, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['bookmark']['article_title'], 'this is andela')
        self.assertEqual(response.data['bookmark']['id'], 32)
        self.assertEqual(response.data['bookmark']['article_id'], 1)
        self.assertEqual(response.data['bookmark']['username'], 'adminuser')

    def test_returns_error_if_user_attempts_to_bookmark_twice(self):
        url = '/api/articles/1/bookmarks/'
        self.client.post(url, HTTP_AUTHORIZATION=self.auth_header, format="json")
        response = self.client.post(url, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn(response.data['error'], "You already bookmarked this Article")

    def test_api_gets_bootmarks_for_a_user(self):
        url = reverse("list_bookmarks")
        url_create = '/api/articles/1/bookmarks/'
        self.client.post(url_create, HTTP_AUTHORIZATION=self.auth_header, format="json")
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data['bookmarks'], list)

    def test_api_gets_one_bookmark(self):
        url_create = '/api/articles/1/bookmarks/'
        url = '/api/bookmarks/30/'
        self.client.post(url_create, HTTP_AUTHORIZATION=self.auth_header, format="json")
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, 200)

    def test_api_deletes_a_bookmark(self):
        url = '/api/bookmarks/30/delete/'
        response = self.client.delete(url, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, 200)
    
    def test_returns_error_if_article_doesnot_exist_on_bookmarking(self):
        url = '/api/articles/1000/bookmarks/'
        response = self.client.post(url, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, 404)
        self.assertIn("Article does not exist", str(response.data))

    def test_returns_error_if_no_bookmark_is_found(self):
        url = reverse('list_bookmarks')
        url_d = '/api/bookmarks/30/delete/'
        self.client.delete(url_d, HTTP_AUTHORIZATION=self.auth_header, format="json")
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, 404)
        self.assertIn("No bookmarks found", str(response.data))

    def test_returns_error_if_user_tries_to_delete_a_bookmark_they_did_not_create(self):
        url = '/api/bookmarks/31/delete/'
        response = self.client.delete(url, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, 403)
        self.assertIn("You can not perform this action", str(response.data))

    def test_returns_an_error_if_the_user_tries_to_get_a_bokkmark_that_is_not_theirs(self):
        url = '/api/bookmarks/31/'
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['message'], 'Bookmark not found')
