from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

from authors.apps.articles.models import Article
from .models import Comment, Likes
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


class Like(APIView):
    """
    create and get likes.
    """

    permission_classes = (IsAuthenticated, )

    def get_comment(self, comment_id):
        """search for a comment by id."""
        try:
            return Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            raise NotFound({"error": "The comment does not exist."})

    def get_like(self, comment_id, username):
        try:
            return Likes.objects.get(comment=comment_id,commenter_id=username)
        except Likes.DoesNotExist:
            return None

    def get(self, request, **kwargs):
        """Method to check for your like on a comment"""
        like = self.get_like(kwargs['comment_id'], request.user.username)
        if like:
            return Response({"status":True}, status=status.HTTP_200_OK)
        return Response({"status":False}, status=status.HTTP_200_OK)

    def post(self, request, **kwargs):
        """ Method to like a specific comment."""
        comment = self.get_comment(kwargs['comment_id'])
        my_like = self.get_like(kwargs['comment_id'], request.user.username)
        if comment.author.username == request.user.username:
            return Response({
                "message": "You can not like your own comment."
            }, status=status.HTTP_403_FORBIDDEN)
        elif not my_like:
            like = Likes(commenter_id=request.user.username,
                like=1, comment=comment)
            like.save()
            Comment.objects.filter(id=kwargs['comment_id']).update(
                likes_counter=comment.likes_counter + 1)
            return Response({"success": "You have successfully liked this comment."},
                            status=status.HTTP_200_OK)
        else:
            my_like.delete()
            Comment.objects.filter(
                id=kwargs['comment_id']).update(likes_counter=comment.likes_counter - 1)
            return Response({"message": "Your like has been cancelled"},
                            status=status.HTTP_200_OK)

