from django.db import models
from authors.apps.authentication.models import User
from authors.apps.articles.models import Article


class Rate(models.Model):

    article = models.ForeignKey(Article, related_name='articles',
                                on_delete=models.CASCADE)
    user = models.ForeignKey(User, to_field='username',
                             on_delete=models.CASCADE, null=False)
    rating = models.IntegerField(null=False, default=0)

    def __str__(self):
        return str(self.rating)
