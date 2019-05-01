from django.db import models
from authors.apps.authentication.models import User
from authors.apps.articles.models import Article


class Favorites(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

