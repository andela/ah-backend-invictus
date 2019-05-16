from django.db.models.signals import post_save
from django.db import models
from django.dispatch import receiver
from django.conf import settings

from authors.settings import pusher
from authors.apps.articles.models import Article, Like_Dislike
from authors.apps.favorites.models import Favorites
from authors.apps.profiles.models import Follow
from authors.apps.comments.models import Comment
from authors.apps.authentication.models import User


class PushNotification(models.Model):
    """ class for push notifications """

    receiver = models.ForeignKey(
        User, to_field='username', on_delete=models.CASCADE)
    message = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """ method returns sting rep of pushnotification"""
        return self.message


def send_author_push_notifications(sender, instance, created, **kwargs):
    """ function sends notification to author
        comment, like,dislike,follow and favorite
    """
    notification = {}
    if isinstance(instance, Favorites):
        article = Article.objects.filter(id=instance.article.id).first()
        author = article.author
        notification['message'] = "Your article with title '{}' has been favorited".format(
            instance.article)
        notification = PushNotification(
            receiver=author, message=notification['message']
        )
        notification.save()
        pusher.trigger(u'a_channel', u'an_event', {u'message': notification.message,
                                                   u'user': notification.receiver.username,
                                                   u'action':'favorite'})
    if isinstance(instance, Like_Dislike):
        article = Article.objects.filter(id=instance.article.id).first()
        choice = instance.like_or_dislike
        if choice == 1:
            choice = 'liked'
        else:
            choice = 'disliked'
        author = article.author
        notification['message'] = "Your article with title '{}' has been {}".format(
            instance.article, choice)
        notification = PushNotification(
            receiver=author, message=notification['message']
        )
        notification.save()
        pusher.trigger(u'a_channel', u'an_event', {u'message': notification.message,
                                                   u'user': notification.receiver.username,
                                                   u'action':choice})

    if isinstance(instance, Comment):
        article = Article.objects.filter(id=instance.article.id).first()
        author = article.author
        notification['message'] = "Your article with title '{}' has been commented on".format(
            instance.article)
        notification = PushNotification(
            receiver=author, message=notification['message']
        )
        notification.save()
        pusher.trigger(u'a_channel', u'an_event', {u'message': notification.message,
                                                   u'user': notification.receiver.username,
                                                   u'action':'comment'})

    if isinstance(instance, Follow):
        followed_user = instance.followed
        notification['message'] = "You have a new follower {}".format(
            instance.follower.username)
        notification = PushNotification(
            receiver=followed_user, message=notification['message']
        )
        notification.save()
        pusher.trigger(u'a_channel', u'an_event', {u'message': notification.message,
                                                   u'user': notification.receiver.username,
                                                   u'action':'follow'})


post_save.connect(send_author_push_notifications, sender=Favorites)
post_save.connect(send_author_push_notifications, sender=Like_Dislike)
post_save.connect(send_author_push_notifications, sender=Comment)
post_save.connect(send_author_push_notifications, sender=Follow)
