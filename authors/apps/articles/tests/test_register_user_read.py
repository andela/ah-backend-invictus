from django.urls import reverse
from .base import BaseTestCase


class AddReadTestCase(BaseTestCase):
    """
    TestCase class for user reads functionality
    """

    def test_api_adds_a_user_read_for_an_article(self):
        """
        Method tests if the api registers a user read
        """
        url = reverse('add_user_read')
        data = {"article_id": 37}
        create_url = reverse('articles-list-create')
        response = self.client.post(
            create_url, self.create_article_data, HTTP_AUTHORIZATION=self.auth_header, format="json")
        response = self.client.post(
            url, data, HTTP_AUTHORIZATION=self.edna_auth_header, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("User read recorded", str(response.data))

    def test_api_returns_an_error_if_the_user_tries_to_register_a_read_again(self):
        """
        Method tests if the api returns an error if the user tries 
        to register a read twice
        """
        url = reverse('add_user_read')
        data = {"article_id": 38}
        create_url = reverse('articles-list-create')
        response = self.client.post(
            create_url, self.create_article_data, HTTP_AUTHORIZATION=self.auth_header, format="json")
        response = self.client.post(
            url, data, HTTP_AUTHORIZATION=self.edna_auth_header, format="json")
        response = self.client.post(
            url, data, HTTP_AUTHORIZATION=self.edna_auth_header, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("User read exists", str(response.data))

    def test_error_register_read_article_not_found(self):
        """
        Method tests if the api returns a 404 not found 
        error if the user tries to register a read for an 
        article that doesnot exist
        """
        url = reverse('add_user_read')
        data = {"article_id": 336}
        response = self.client.post(
            url, data, HTTP_AUTHORIZATION=self.edna_auth_header, format="json")
        self.assertEqual(response.status_code, 404)
        self.assertIn("Article doesnot exist", str(response.data))

    def test_returns_error_if_author_tries_to_read_their_article(self):
        """
        Method tests if the api returns an error if 
        an author tries to read their own article
        """
        url = reverse('add_user_read')
        data = {"article_id": 39}
        create_url = reverse('articles-list-create')
        response = self.client.post(
            create_url, self.create_article_data, HTTP_AUTHORIZATION=self.auth_header, format="json")
        response = self.client.post(
            url, data, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Author can not read their own article", str(response.data))

    def test_returns_error_if_id_is_missing_on_register_read(self):
        """
        Method tests if the api returns an error if an id is
        not provided on registering a read
        """
        url = reverse('add_user_read')
        create_url = reverse('articles-list-create')
        response = self.client.post(
            create_url, self.create_article_data, HTTP_AUTHORIZATION=self.auth_header, format="json")
        response = self.client.post(
            url,  HTTP_AUTHORIZATION=self.edna_auth_header, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("You must provide an article id to proceed", str(response.data))

    
    def test_user_can_add_a_view(self):
        """
        Method tests if a user can add a view
        """
        url = '/api/articles/41/'
        create_url = reverse('articles-list-create')
        response = self.client.post(
            create_url, self.create_article_data, HTTP_AUTHORIZATION=self.auth_header, format="json")
        response = self.client.get(
            url, HTTP_AUTHORIZATION=self.edna_auth_header, format="json")
        self.assertEqual(response.status_code, 200)

