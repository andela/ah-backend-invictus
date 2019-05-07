from django.db import models
from django.utils.text import slugify
from authors.apps.articles.models import Article
from authors.apps.authentication.models import User


class Bookmark(models.Model):
    """
    Model class for bookmarks
    """
    date_created = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=70, null=True)
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE)
    article_title = models.CharField(max_length=300, null=True)


    def __str__(self):
        return self.article_title
