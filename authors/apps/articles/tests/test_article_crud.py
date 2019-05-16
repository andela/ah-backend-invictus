# Django and Rest framework imports
from django.urls import reverse
from rest_framework import status
# Local imports
from authors.apps.articles.models import Article
from .base import BaseTestCase
from authors.apps.authentication.models import User


class ArticleCrudTest(BaseTestCase):
    """
    Class Test Case for Testing article crud functionality
    """
    # Initialize fixture for the class Test Case
    fixtures = ['authors/apps/articles/fixtures/user.json']


    def test_user_create_article(self):
        """
        Method tests the create article
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_data, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        social_links = response.data['article']['social_links']
        # self.assertIn('https://www.facebook.com/sharer/sharer.php?u=htt', social_links['facebook'])
        self.assertIn('https://www.facebook.com/', social_links['facebook'])
        self.assertIn('https://twitter.com/home?status=htt', social_links['twitter'])
        self.assertIn('mailto:?&subject=Authors%20Haven%', social_links['email'])

    def test_user_create_article_blank_title(self):
        """
        Method tests creating the article with blank title
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_with_blank_title, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertIn("The title field cannot be left blank",
                      str(response.data))

    def test_user_created_article_no_title(self):
        """
        Method tests creating the article with no title field
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_with_no_title, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertIn("This field may not be null", str(response.data))

    def test_user_created_article_blank_description(self):
        """
        Method tests creating the article with blank description field
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_with_blank_description, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertIn("The description field cannot be left blank",
                      str(response.data))

    def test_user_created_article_no_description(self):
        """
        Method tests creating the article with no description field
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_with_no_description, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertIn("This field may not be null", str(response.data))

    def test_only_one_article_created(self):
        """
        Method tests for only one created article
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_data, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(Article.objects.count(), 1)

    def test_get_all_articles(self):
        """
        Method tests for getting all articles
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_data, HTTP_AUTHORIZATION=self.auth_header, format="json")
        url = '/api/articles/all/'
        response = self.client.get(
            url, self.create_article_data, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_article(self):
        """
        Method tests for getting one article
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_data, HTTP_AUTHORIZATION=self.auth_header, format="json")
        article_id = response.data['article']['id']
        url = '/api/articles/{}/retrieve/'.format(article_id)
        response = self.client.get(
            url, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_article(self):
        """
        Method test for updating one article
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_data, HTTP_AUTHORIZATION=self.auth_header, format="json")
        article_id = response.data['article']['id']
        url = '/api/articles/{}/'.format(article_id)
        self.client.put(
            url, self.article_data_no_tags, HTTP_AUTHORIZATION=self.auth_header, format="json")
        response = self.client.put(
            url, self.create_article_data, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_article_new_tags(self):
        """
        Method test for updating one article
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_data, HTTP_AUTHORIZATION=self.auth_header, format="json")
        article_id = response.data['article']['id']
        url = '/api/articles/{}/'.format(article_id)
        response = self.client.put(
            url, self.article_data_new_tags, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_no_permision_to_update_article(self):
        """
        Method tests for permision for updating one article
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_data, HTTP_AUTHORIZATION=self.auth_header, format="json")
        article_id = response.data['article']['id']
        url = '/api/articles/{}/'.format(article_id)
        response = self.client.put(
            url, self.update_article, HTTP_AUTHORIZATION=self.edna_auth_header, format="json")
        self.assertIn(
            "You do not have permission to perform this action", str(response.data))

    def test_no_permision_to_delete_article(self):
        """
        Method tests for permision for deleting one article
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_data, HTTP_AUTHORIZATION=self.auth_header, format="json")
        article_id = response.data['article']['id']
        url = '/api/articles/{}/'.format(article_id)
        response = self.client.delete(
            url, self.update_article, HTTP_AUTHORIZATION=self.edna_auth_header, format="json")
        self.assertEqual(
            'You do not have permision to delete the article',  str(response.data))

    def test_get_article_wrong_id(self):
        """
        Method tests for getting one article with the wrong id
        """
        url = '/api/articles/4/retrieve/'
        response = self.client.get(
            url, self.create_article_data, format="json")
        self.assertIn("That article is not found", str(response.data))

    def test_user_create_article_blank_body(self):
        """
        Method tests creating the article with blank body
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_with_blank_body, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertIn("The body field cannot be left blank",
                      str(response.data))

    def test_user_created_article_no_body(self):
        """
        Method tests creating the article with no body field
        """
        url = '/api/users/login/'
        response = self.client.post(url, self.login_data, format="json")
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_with_no_body, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertIn("This field may not be null", str(response.data))

    def test_user_created_article_short_title(self):
        """
        Method tests creating the article with short title
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.short_title_article, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertIn("Title should be atleast 10 characters",
                      str(response.data))

    def test_valid_status_code_when_token_not_passed_in_header(self):
        """
        Method tests creating the article with short title
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_valid_message_when_token_not_passed_in_header(self):
        """
        Method tests if the token is passed in the header
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_data, format="json")
        self.assertIn('Token is missing.', str(response.data))

    def test_delete_article(self):
        """
        Method tests deleting the article
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_data, HTTP_AUTHORIZATION=self.auth_header, format="json")
        article_id = response.data['article']['id']
        url = '/api/articles/{}/'.format(article_id)
        response = self.client.delete(
            url, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_article_not_found(self):
        """
        Method tests deleting the non existant article
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_data, HTTP_AUTHORIZATION=self.auth_header, format="json")
        url = '/api/articles/1000/'
        response = self.client.delete(
            url, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_article_not_found_message(self):
        """
        Method tests disliking the non existant article
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.create_article_data, HTTP_AUTHORIZATION=self.auth_header, format="json")
        url = '/api/articles/1000/'
        response = self.client.delete(
            url, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
