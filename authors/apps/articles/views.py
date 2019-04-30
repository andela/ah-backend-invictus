from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .renderer import ArticleJSONRenderer
from .models import Article
from .serializers import ArticleSerializer
from .permissions import IsOwnerOrReadOnly


class ListCreateArticles(generics.ListCreateAPIView):
    """
    GET articles/
    POST articles/
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticated, )
    renderer_classes = (ArticleJSONRenderer, )

    def perform_create(self, serializer):

        serializer.save(
            author=self.request.user
        )


class RetrieveUpdateDestroyArticle(generics.RetrieveUpdateDestroyAPIView):
    """
    GET articles/:id/
    PUT articles/:id/
    DELETE articles/:id/
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly, )
    renderer_classes = (ArticleJSONRenderer, )
    err_message = {"errors": "That article is not found"}

    def get(self, request, pk, **kwargs):
        user = request.user
        queryset = Article.objects.all().filter(id=pk)

        if queryset:
            serializer = ArticleSerializer(
                queryset, many=True, context={'request': request})
            return Response(serializer.data)
        return Response(self.err_message, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk, **kwargs):
        user = request.user
        queryset = Article.objects.all().filter(id=pk)
        if queryset:
            if queryset[0].author == user:
                self.perform_destroy(queryset)
                return Response("You have succesfully deleted the article")
            return Response("You do not have permision to delete the article")
        return Response(self.err_message, status=status.HTTP_404_NOT_FOUND)
