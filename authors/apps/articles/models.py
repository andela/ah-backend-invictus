from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone

from authors.apps.authentication.models import User
from authors.apps.article_tags.models import ArticleTag
from .utils import unique_slug_generator


class Article(models.Model):
    """
    Model class for creating an article
    """

    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True,
                            null=True)
    description = models.TextField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True)
    likes_count = models.IntegerField(default=0)
    dislikes_count = models.IntegerField(default=0)
    favorited = models.BooleanField(default=False)
    favorite_count = models.IntegerField(default=0)
    tagList = models.ManyToManyField(ArticleTag, related_name='articles')
    author = models.ForeignKey(
        User, to_field='username', on_delete=models.CASCADE, null=False)

    def __str__(self):
        """
        return string representation of the article
        model class
        """
        return self.title


def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(slug_generator, sender=Article)


class Like_Dislike(models.Model):
    """
    Model class for liking or disliking an article
    """
    date_liked = models.DateTimeField(auto_now_add=True, editable=False)
    like_or_dislike = models.IntegerField()
    reviewer = models.ForeignKey(
        User, to_field='username', on_delete=models.CASCADE, null=False)
    article = models.ForeignKey(
        Article, to_field='id', on_delete=models.CASCADE, null=False
    )
