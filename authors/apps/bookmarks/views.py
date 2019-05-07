from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from authors.apps.articles.models import Article
from .serializers import BookmarkSerializer
from .models import Bookmark


class GetBookMarks:

    @staticmethod
    def get_bookmarks(req):
        try:
            bookmarklist = Bookmark.objects.all()
            return bookmarklist
        except Bookmark.DoesNotExist:
            return None


class CreateBookmark(CreateAPIView):
    """
    View class for creating a bookmark
    """
    serializer_class = BookmarkSerializer

    def create(self, request, pk):
        """
        Method creates a new bookmark
        """
        try:
            user = request.user
            bookmarks = GetBookMarks.get_bookmarks(request)
            article = Article.objects.get(pk=pk)
            for bookmark in bookmarks:
                if bookmark.user_id.id == user.id and\
                        bookmark.article_id.id == int(article.id):
                    return Response({'error': 'You already bookmarked this Article'},
                                    status=status.HTTP_400_BAD_REQUEST)
            data = {'user_id': user.id, 'username': user.username,
                    'article_title': article.title, 'article_id': article.id}
            serializer = BookmarkSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response_data = serializer.data
            response_data.pop('user_id')
            return Response({'bookmark': response_data},
                            status=status.HTTP_201_CREATED)
        except:
            error = {'error': 'Article does not exist'}
            raise NotFound(detail=error)


class ListBookmarks(ListAPIView):
    """
    View class for fetching all user bookmarks
    """
    serializer_class = BookmarkSerializer

    def get(self, request):
        """
        Method gets a list of bookmarks of the current user
        """
        user = request.user
        bookmarks = Bookmark.objects.filter(user_id=user.id)
        if bookmarks:
            serializer = BookmarkSerializer(bookmarks, many=True)
            return Response({'bookmarks': serializer.data},
                            status=status.HTTP_200_OK)
        return Response({'message': 'No bookmarks found'},
                        status=status.HTTP_404_NOT_FOUND)


class RetrieveBookmark(RetrieveAPIView):
    """
    View class for getting one bookmark
    """
    serializer_class = BookmarkSerializer
    queryset = Bookmark.objects.all()

    def retrieve(self, request, *args, **kwargs):
        """
        Method gets one bookmark
        """
        instance = self.get_object()
        bookmark_user = instance.user_id.id
        user = request.user
        if user.id != bookmark_user:
            return Response({'message': 'Bookmark not found'},
            status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance)
        return Response({'bookmark': serializer.data},
                        status=status.HTTP_200_OK)


class DeleteBookmark(DestroyAPIView):
    """
    View class for deleting a bookmark
    """
    serializer_class = BookmarkSerializer
    queryset = Bookmark.objects.all()

    def destroy(self, request, *args, **kwargs):
        """
        Method deletes a bookmark
        """
        instance = self.get_object()
        bookmark_user = instance.user_id.id
        user = request.user
        if user.id != bookmark_user:
            return Response({'error': 'You can not perform this action'},
            status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response({"message": "Bookmark deleted"},
                        status=status.HTTP_200_OK)
