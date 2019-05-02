from django.db import models


class ArticleTag(models.Model):
    """
    Article tag model class
    """
    article_tag_text = models.CharField(max_length=70, unique=True)

    def __str__(self):
        """
        Returns a string representation
        of the Article tag model class
        """
        return self.article_tag_text
