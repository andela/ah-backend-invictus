from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

from authors.apps.articles.models import Article
from .models import Comment
from .serializers import CommentSerializer


class ListCreateComment(APIView):
    """
    GET Comments/
    POST Comment/
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = CommentSerializer

    def get_article(self, article_id):
        """
        This method returns an article by its id.
        """
        try:
            return Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            raise NotFound({"error": "Article not found."})

    def post(self, request, **kwargs):
        """
        This method adds a comment to a particular article.
        """
        article = self.get_article(kwargs['article_id'])
        comment = request.data.get('comment', {})
        comment['article'] = article.id
        serializer = CommentSerializer(data=comment)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user)
        return Response({
            "comment": serializer.data,
            "message": "Comment successfully created."
        }, status=status.HTTP_201_CREATED)

    def get(self, request, **kwargs):
        """
        This method returns a list of comments on an article.
        """
        self.get_article(kwargs['article_id'])
        queryset = Comment.objects.filter(article=self.kwargs['article_id'])
        serializer = CommentSerializer(queryset, many=True)
        return Response({
            "comments": serializer.data}, status=status.HTTP_200_OK)


class RetrieveUpdateDeleteComment(APIView):
    """
    GET Comment/
    Update Comment/
    Delete Comment/
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_article(self, article_id):
        """
        Returns an article by its id.
        """
        try:
            return Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            raise NotFound({"error": "Article not found."})

    def get_comment(self, pk):
        """
        This method returns a comment by its id.
        """
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise NotFound({"error": "Comment not found."})

    def get(self, request, pk, article_id, **kwargs):
        """
        This method returns a single comment.
        """
        self.get_article(article_id)
        comment = self.get_comment(pk)
        serializer = CommentSerializer(comment)
        return Response({"comment": serializer.data})

    def put(self, request, pk, article_id):
        """
        This method updates a single comment.
        """
        article = self.get_article(article_id)
        comment = self.get_comment(pk)
        if comment.author.username == request.user.username:
            data = {}
            data['article'] = article.id
            data['body'] = request.data['comment']['body']
            serializer = CommentSerializer(comment, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                "comment": serializer.data,
                "message": "Comment successfully updated."
            }, status=status.HTTP_200_OK)
        return Response({
            "error": "You do not have permissions to edit this comment."
        }, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk, article_id):
        """
        This method deletes a single comment.
        """
        self.get_article(article_id)
        comment = self.get_comment(pk)
        if comment.author.username == request.user.username:
            comment.delete()
            return Response({
                "message": "Comment successfully deleted."
            }, status=status.HTTP_200_OK)
        return Response({
            "error": "You do not have permissions to delete this comment."
        }, status=status.HTTP_403_FORBIDDEN)
