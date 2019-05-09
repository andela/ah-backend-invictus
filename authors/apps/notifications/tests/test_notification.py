# from .base import BaseTestCase
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from ..models import UserNotification
from authors.apps.authentication.models import User
from authors.apps.articles.models import Article, Like_Dislike
from authors.apps.profiles.models import Follow
from authors.apps.comments.models import Comment
from authors.apps.favorites.models import Favorites


class TestSendNotificationsTestCase(APITestCase):
    """ class to test getting user notifications. """
    fixtures = ['authors/apps/notifications/fixtures/notification_data.json']

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            username='test1', email='test1@example.com', password='12345678', email_verified=True
        )
        self.user_author = User.objects.create(
            username='mary1', email='test2@example.com', password='12345678', email_verified=True
        )
        self.follow = Follow.objects.create(
            follower=self.user, followed=self.user_author
        )
        self.article = Article.objects.create(
            title="this is andela",
            description="edna",
            body="There was no TIA chant.",
            author=self.user_author
        )
        self.notification_data = UserNotification.objects.create(
            reciever=self.user,
            message="Airtcles has new comment"
        )
        self.favorite = Favorites.objects.create(article=self.article, user=self.user)
       
    def test_get_user_notification_new_article(self):
        """Tests that particular user gets notification."""
        self.article = Article.objects.create(
            title="this is andela",
            description="edna",
            body="There was no TIA chant.",
            author=self.user_author
        )
        self.client.force_authenticate(user=self.user)
        url = reverse('notifications')
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_notification_new_comment(self):
        """Test get notification for new comment"""
        self.comment = Comment.objects.create(
            body="comment by andela",
            article_id=self.article.id,
            author_id=self.user_author.id
        )
        self.client.force_authenticate(user=self.user)
        url = reverse('notifications')
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_notification_new_follower(self):
        """Test get notification for new follower"""
        self.follower = Follow.objects.create(
            follower=self.user_author,
            followed=self.user
        )
        self.client.force_authenticate(user=self.user)
        url = reverse('notifications')
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_notification_on_like(self):
        """Test get notification for new follower"""
        self.like_dislike = Like_Dislike.objects.create(
            date_liked="2019-05-02T05:03:36.898341Z",
            like_or_dislike=1,
            reviewer=self.user,
            article=self.article
        )
        self.client.force_authenticate(user=self.user)
        url = reverse('notifications')
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_notification_on_dislike(self):
        """Test get notification for new follower"""
        self.like_dislike = Like_Dislike.objects.create(
            date_liked="2019-05-02T05:03:36.898341Z",
            like_or_dislike=-1,
            reviewer=self.user,
            article=self.article
        )
        self.client.force_authenticate(user=self.user)
        url = reverse('notifications')
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_notification(self):
        """Test get single notification."""
        self.notification = UserNotification.objects.create(
            id=2,
            reciever=self.user,
            message="Airtcles has new comment"
        )
        self.notification.save()
        self.client.force_authenticate(user=self.user)
        url = '/api/notifications/2/'
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_notification_not_found(self):
        """Test get single notification not found."""
        self.notification = UserNotification.objects.create(
            reciever=self.user,
            message="Airtcles has new comment"
        )
        self.client.force_authenticate(user=self.user)
        url = '/api/notifications/1000/'
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_notification_model_returns_string(self):
        """Tests that model returns a string."""
        self.assertTrue(self.notification_data.message,
                        str(self.notification_data))

    def test_deactivate_notification(self):
        """Tests that notifications are deactivated."""
        url = reverse('set_notifications')
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"],
                         "You have sucessfully turned notifications off")

    def test_activate_notification(self):
        """Tests that notifications are activated."""
        url = reverse('set_notifications')
        self.client.force_authenticate(user=self.user)
        self.client.post(url, format="json")
        response = self.client.post(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"],
                         "You have sucessfully turned notifications on")
