from django.urls import reverse
from rest_framework import status
from .base import BaseTestCase


class TagTestCase(BaseTestCase):
    def test_user_create_article_tag(self):
        """
        Method tests the create tag when an article is created
        """
        url = reverse('articles-list-create')
        response = self.client.post(
            url, self.data.create_arcticle, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['article']['tagList'][0], "techville")
        self.assertIsInstance(response.data['article']['tagList'], list)

    def test_get_all_tags(self):
        """
        Methods tests that api returns all tags
        """
        url = reverse('tags')
        create_url = reverse('articles-list-create')
        self.client.post(
            create_url, self.data.create_arcticle, HTTP_AUTHORIZATION=self.auth_header,
            format="json")
        response = self.client.get(
            url, HTTP_AUTHORIZATION=self.auth_header, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["article_tag_text"], "techville")

    def test_can_update_an_article_tag_list(self):
        create_url = reverse('articles-list-create')
        update_url = '/api/articles/1/'
        self.client.post(
            create_url, self.data.create_arcticle, HTTP_AUTHORIZATION=self.auth_header,
            format="json")
        response = self.client.put(
            update_url, self.data.update_tag, HTTP_AUTHORIZATION=self.auth_header,
            format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['tagList'][0], "Microsoft")
        self.assertIsInstance(response.data['tagList'], list)

    def test_resets_the_taglist_when_a_user_provides_an_empty_taglist(self):
        create_url = reverse('articles-list-create')
        update_url = '/api/articles/3/'
        res = self.client.post(
            create_url, self.data.create_arcticle, HTTP_AUTHORIZATION=self.auth_header,
            format="json")
        response = self.client.put(
            update_url, self.data.empty_tag_list, HTTP_AUTHORIZATION=self.auth_header,
            format="json") 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['tagList'], [])
