from rest_framework import serializers
from urllib.parse import quote
from django.urls import reverse
from authors.apps.article_tags.models import ArticleTag
from .models import Article, Report
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
    social_links = serializers.SerializerMethodField()

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

    def get_social_links(self, insitance):
        links = dict()
        article_url = self.context['request'].build_absolute_uri(
            reverse("article-get", kwargs={'pk':insitance.pk}))
        article_url_quote = quote(article_url)
        # facebook url
        facebook_url = f"https://www.facebook.com/sharer/sharer.php?u={article_url_quote}"
        links['facebook'] = facebook_url
        # twitter url
        twitter_url = f"https://twitter.com/home?status={article_url_quote}"
        links['twitter'] = twitter_url
        # email url
        subject = quote(f"Authors Haven: {insitance.title}")
        body = quote(
            f"Follow Link To View Article {article_url}")
        email_link = f'mailto:?&subject={subject}&body={body}'
        links['email'] = email_link
        return links

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
            'author',
            'tagList',
            'read_time',
            'social_links',
        )
        read_only_fields = ('created_at', 'updated_at', 'author',
                            'favorited', 'favorite_count', 'slug',
                            'social_links', 'read_time')


class ReportSerializer(serializers.ModelSerializer):
    """ Class to serialize the data in the report body """
    reason = serializers.CharField(
        required=True,
        error_messages={
            "required": "The reason field is required",
            "blank": "The reason field cannot be left blank"
        }
    )

    class Meta:
        """class for returning our fields."""
        model = Report
        fields = '__all__'
