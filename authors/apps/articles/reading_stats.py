from django.db import models
from django.utils.timezone import now
from authors.apps.articles.models import Article
from .models import User
import datetime


class UserViews(models.Model):
    """
    Model class to capture user views
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    viewed_on = models.DateTimeField(auto_now_add=True)


class UserReads(models.Model):
    """
    Model class to capture user reads
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    read_on = models.DateTimeField(auto_now_add=True)
