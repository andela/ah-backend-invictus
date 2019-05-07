from rest_framework import serializers

from authors.apps.article_tags.models import ArticleTag
from .models import Article
from .validations import ValidateArticleCreation


class ArticleSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        required=True,
        error_messages={
            "required": "The title field is required",
            "blank": "The title field cannot be left blank"
        }
    )
    description = serializers.CharField(
        required=True,
        error_messages={
            "required": "The description field is required",
            "blank": "The description field cannot be left blank"
        }
    )
    body = serializers.CharField(
        required=True,
        error_messages={
            "required": "The body field is required",
            "blank": "The body field cannot be left blank"
        }
    )
    tagList = serializers.SlugRelatedField(
        many=True,
        queryset=ArticleTag.objects.all(),
        slug_field='article_tag_text'
    )

    def validate(self, data):
        title = data.get('title', None)
        description = data.get('description', None)
        body = data.get('body', None)

        validator = ValidateArticleCreation()
        validator.validate_title(title)
        validator.validate_title(description)
        validator.validate_title(body)

        return {
            'title': title,
            'body': body,
            'description': description
        }

    class Meta:
        """class for returning our fields."""

        model = Article
        fields = (
            'id',
            'title',
            'description',
            'body',
            'slug',
            'created_at',
            'updated_at',
            'likes_count',
            'dislikes_count',
            'favorited',
            'favorite_count',
            'tagList',
            'author'
        )
        read_only_fields = ('created_at', 'updated_at', 'author',
                            'favorited', 'favorite_count', 'slug')
