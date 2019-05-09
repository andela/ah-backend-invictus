from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """
    This class maps the `Comment` model instance
    into JSON format.
    """

    author = serializers.ReadOnlyField(source='author.username')
    first_index = serializers.IntegerField(min_value=0, required=False)
    last_index = serializers.IntegerField(min_value=0, required=False)

    class Meta:
        model = Comment
        # List all of the comment fields that could possibly be included in a
        # request or response, including fields specified explicitly above.
        fields = '__all__'


class CommentEditHistorySerializer(serializers.ModelSerializer):
    """
    This class maps the `History` model instance
    into JSON format.
    """

    class Meta:
        model = Comment
        # List the comments update history fields that should be returned.
        fields = (
            'id',
            'body',
            'article_id',
            'created_at',
            'updated_at'
        )
