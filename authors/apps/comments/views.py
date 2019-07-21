from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Comment, Likes
from .serializers import CommentSerializer, CommentEditHistorySerializer
from .utils import get_article, get_comment
from drf_yasg.utils import swagger_auto_schema


class ListCreateComment(APIView):
    """
    GET Comments/
    POST Comment/
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = CommentSerializer

    @swagger_auto_schema(
        operation_description="Add a comment to an article.",
        operation_id="Add a comment to an article.",
        request_body=serializer_class,
        responses={200: serializer_class(many=False), 400: "BAD REQUEST"},
    )
    def post(self, request, **kwargs):
        """
        This method adds a comment to a particular article.
        """
        article = get_article(kwargs['article_id'])
        comment = request.data.get('comment', {})
        comment['article'] = article.id
        first_index = comment.get('first_index', 0)
        last_index = comment.get('last_index', 0)
        if "first_index" in comment and "last_index" in comment:
            if not isinstance(first_index, int) or not isinstance(last_index, int):
                return Response(
                    {"Error": "First index and last index must be integers."},
                    status.HTTP_400_BAD_REQUEST)
            if first_index > len(article.body) or last_index > len(article.body):
                return Response({
                    "Error": "You should only highlight within the article body."
                }, status.HTTP_400_BAD_REQUEST)
            if int(first_index) > int(last_index):
                return Response(
                    {"Error": "First index should be less than Last index."},
                    status.HTTP_400_BAD_REQUEST)
            highlighted_section = article.body[first_index:last_index]
            comment['highlighted_text'] = highlighted_section
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
        get_article(kwargs['article_id'])
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

    def get(self, request, pk, **kwargs):
        """
        This method returns a single comment.
        """
        get_article(kwargs['article_id'])
        comment = get_comment(pk)
        serializer = CommentSerializer(comment)
        return Response({"comment": serializer.data})

    def put(self, request, pk, **kwargs):
        """
        This method updates a single comment.
        """
        article = get_article(kwargs['article_id'])
        comment = get_comment(pk)
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

    def delete(self, request, pk, **kwargs):
        """
        This method deletes a single comment.
        """
        get_article(kwargs['article_id'])
        comment = get_comment(pk)
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

    def get_like(self, pk, username):
        try:
            return Likes.objects.get(comment=pk, commenter_id=username)
        except Likes.DoesNotExist:
            return None

    def get(self, request, **kwargs):
        """Method to check for your like on a comment."""
        like = self.get_like(kwargs['pk'], request.user.username)
        if like:
            return Response({"status": True}, status=status.HTTP_200_OK)
        return Response({"status": False}, status=status.HTTP_200_OK)

    def post(self, request, **kwargs):
        """Method to like a specific comment."""
        comment = get_comment(kwargs['pk'])
        my_like = self.get_like(kwargs['pk'], request.user.username)
        if comment.author.username == request.user.username:
            return Response({
                "message": "You can not like your own comment."
            }, status=status.HTTP_403_FORBIDDEN)
        elif not my_like:
            like = Likes(commenter_id=request.user.username,
                         like=1, comment=comment)
            like.save()
            Comment.objects.filter(id=kwargs['pk']).update(
                likes_counter=comment.likes_counter + 1)
            return Response({
                "success": "You have successfully liked this comment."
            }, status=status.HTTP_200_OK)
        else:
            my_like.delete()
            Comment.objects.filter(id=kwargs['pk']).update(
                                   likes_counter=comment.likes_counter - 1)
            return Response({"message": "Your like has been cancelled"},
                            status=status.HTTP_200_OK)


class CommentEditHistoryAPIView(APIView):
    """
    GET History/
    Return comment updates history by a given user
    on a particular article.
    """

    permission_classes = (IsAuthenticated, )

    def get(self, request, **kwargs):
        """
        Return all comment update history.
        """
        get_article(kwargs['article_id'])
        comment = get_comment(kwargs['pk'])
        data = comment.history.all()
        serializer = CommentEditHistorySerializer(data, many=True)
        return Response({
            "update_history": serializer.data}, status=status.HTTP_200_OK)
