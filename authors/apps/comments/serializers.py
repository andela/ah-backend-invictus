from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """
    This class maps the `Comment` model instance
    into JSON format.
    """

    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        # List all of the comment fields that could possibly be included in a
        # request or response, including fields specified explicitly above.
        fields = '__all__'
