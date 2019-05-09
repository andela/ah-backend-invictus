from django.db import models

from simple_history.models import HistoricalRecords
from authors.apps.authentication.models import User
from authors.apps.articles.models import Article


class Comment(models.Model):
    """
    This class represents the comment model.
    """

    article = models.ForeignKey(Article, related_name='comments',
                                on_delete=models.CASCADE)
    body = models.TextField()
    author = models.ForeignKey(User, related_name='author',
                               on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes_counter = models.IntegerField(default=0)
    history = HistoricalRecords()

    def __str__(self):
        """
        This method returns a string representation of the
        `Comment` model instance.
        """
        return self.body


class Likes(models.Model):
    """
    Model class for liking a specific comment.
    """
    commenter = models.ForeignKey(
        User, to_field='username', on_delete=models.CASCADE, null=False)
    like = models.IntegerField()
    comment = models.ForeignKey(
        Comment, to_field='id', on_delete=models.CASCADE, null=False
    )
    liked_at = models.DateTimeField(auto_now_add=True, editable=False)
