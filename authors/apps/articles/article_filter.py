import django_filters
from django_filters import rest_framework as filters
from .models import Article


class ArticleFilter(django_filters.FilterSet):
    """ class to manage filter by author, taglist, title"""

    title = filters.CharFilter(lookup_expr='icontains')
    author = filters.CharFilter('author__username', lookup_expr='icontains')
    tag = filters.CharFilter('tagList__article_tag_text')

    class Meta:
        model = Article
        fields = ('title', 'author', 'tag', )
