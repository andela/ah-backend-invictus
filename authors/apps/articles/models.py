from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone

from authors.apps.authentication.models import User
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
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    favorited = models.BooleanField(default=False)
    favorite_count = models.IntegerField(default=0)
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
