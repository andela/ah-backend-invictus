from django.db.models.signals import post_save
from django.dispatch import receiver

from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from django.db import models
from authors.apps.favorites. models import Favorites
from authors.apps.comments.models import Comment
from authors.apps.authentication.models import User
from authors.apps.articles.models import Article, Like_Dislike
from authors.apps.profiles.models import Follow


class UserNotification(models.Model):
    """Class for notifications."""

    reciever = models.ForeignKey(User, to_field='username', on_delete=models.CASCADE)
    message = models.CharField(max_length=255, null=True)
    link = models.CharField(max_length=255, null=True)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Method returns sting representation of product."""
        return self.message


class NotificationSetting(models.Model):
    """Class to configure notifications."""
    user = models.ForeignKey(User, to_field='username', on_delete=models.CASCADE)
    get_notification = models.BooleanField(default=True)


@receiver(post_save, sender=User)
def set_notifications(sender, instance, created, **kwargs):
    """Functions creates notifications setting instance."""
    if created:
        NotificationSetting.objects.create(user=instance)


def email_notification(body):
    """Function for email notification."""
    subject = body["subject"]
    message = body["message"]
    from_email = settings.EMAIL_HOST_USER
    email_to = body['email_to']
    email = EmailMultiAlternatives(
        subject,
        message,
        from_email,
        [email_to]
    )
    email.send()


@receiver(post_save, sender=Article)
def send_notification_new_article(sender, instance, created, **kwargs):
    """
    Function sends notification to user.
    when : user followed writes new article.
    """
    if created:
        email_body = {}
        users_following = Follow.objects.filter(followed=instance.author)
        link = "/api/articles/{}/".format(instance.id)
        email_body["message"] = '{} created a new article'.format(instance.author.username)
        for user in users_following:
            user_get_notification = NotificationSetting.objects.filter(
                user=user.follower, get_notification=True).exclude(user_id=instance.author.id)
            if user_get_notification:
                notification = UserNotification.objects.create(
                    reciever=user.follower,
                    message=email_body["message"],
                    link=link
                    )
                notification.save()
                email_body["subject"] = "Notification for new Article"
                email_body["email_to"] = user.follower.email
                email_notification(email_body)


@receiver(post_save, sender=Comment)
def send_notification_new_comment(sender, instance, created, **kwargs):
    """Function sends notification to user when favorite article gets comment."""
    if created:
        email_body = {}
        users_favorited = Favorites.objects.filter(
            article=instance.article_id).exclude(user_id=instance.author.id)
        article_title = instance.article
        article_id = instance.article.id
        comment_id = instance.id
        author = instance.author.username
        email_body["message"] = f"Article with title {article_title} has a new comment by {author}"
        link = "/api/articles/{}/comments/{}/".format(article_id, comment_id)
        for user in users_favorited:
            user_get_notification = NotificationSetting.objects.filter(
                user=user.user, get_notification=True)
            if user_get_notification:
                notification = UserNotification.objects.create(
                    reciever=user.user,
                    message=email_body["message"],
                    link=link)
                notification.save()
                email_body["subject"] = "Notification for new comment"
                email_body["email_to"] = user.user.email
                email_body["link"] = link
                email_notification(email_body)


@receiver(post_save, sender=Follow)
def send_notification_new_user_gets_follower(sender, instance, created, **kwargs):
    """Function sends notification to user when gets a new follower."""
    if created:
        email_body = {}
        email_body["message"] = "You have a new follower"
        followed_user = instance.followed
        user_get_notification = NotificationSetting.objects.filter(
                user=followed_user, get_notification=True)
        if user_get_notification:
            notification = UserNotification.objects.create(
                reciever=followed_user,
                message=email_body["message"]
                )
            notification.save()
            email_body["subject"] = "Notification for new Follower"
            email_body["email_to"] = followed_user.email
            email_notification(email_body)


@receiver(post_save, sender=Like_Dislike)
def send_notification_when_airticle_gets_like(sender, instance, created, **kwargs):
    """Function sends notification to article  gets a new like."""
    if created:
        handle_update_create_signals(instance)
    if not created:
        handle_update_create_signals(instance)


def handle_update_create_signals(instance):
    article = Article.objects.filter(id=instance.article.id).first()
    email_body = {}
    choice = instance.like_or_dislike
    if choice == 1:
        choice = 'liked'
    else:
        choice = 'disliked'
    author = article.author
    email_body["message"] = "Your article with title '{}' has been {}".format(
        instance.article, choice)
    user_get_notification = NotificationSetting.objects.filter(
            user=article.author, get_notification=True)
    if user_get_notification:
        notification = UserNotification.objects.create(
            reciever=author,
            message=email_body["message"]
            )
        notification.save()
        email_body["subject"] = "Notification for Article like or dislike"
        email_body["email_to"] = author.email
        email_notification(email_body)