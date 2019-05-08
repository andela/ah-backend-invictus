from rest_framework import serializers
from authors.apps.bookmarks.models import Bookmark


class BookmarkSerializer(serializers.ModelSerializer):
    """
    Srializer class for bookmarks
    """
    class Meta:
        model = Bookmark
        fields = ('id', 'user_id', 'article_id', 'username',
                  'article_title', 'date_created')
