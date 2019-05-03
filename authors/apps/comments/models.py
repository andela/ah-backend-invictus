from django.db import models

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

    def __str__(self):
        """
        This method returns a string representation of the
        `Comment` model instance.
        """
        return self.body
