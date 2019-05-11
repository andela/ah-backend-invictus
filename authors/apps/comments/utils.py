from rest_framework.exceptions import NotFound

from authors.apps.articles.models import Article
from .models import Comment


def get_article(article_id):
    """
    Returns an article by its id.
    """
    try:
        return Article.objects.get(id=article_id)
    except Article.DoesNotExist:
        raise NotFound({"error": "Article not found."})


def get_comment(pk):
    """
    This method returns a comment by its id.
    """
    try:
        return Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        raise NotFound({"error": "Comment not found."})
