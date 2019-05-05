from rest_framework import serializers
from .models import ArticleTag


class ArticleTagSerializer(serializers.ModelSerializer):
    """
    Serializer class for Article Tags
    """
    articles = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug'
    )
    class Meta:
        model = ArticleTag
        fields = ('article_tag_text', 'articles')
