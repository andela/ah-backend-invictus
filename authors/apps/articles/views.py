from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from authors.apps.article_tags.views import ArticleTagView
from authors.apps.article_tags.models import ArticleTag
from .renderer import ArticleJSONRenderer
from .models import Article
from .serializers import ArticleSerializer
from .permissions import IsOwnerOrReadOnly
from .pagination import ArticlePageNumberPagination


class ListCreateArticles(generics.ListCreateAPIView):
    """
    GET articles/
    POST articles/
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticated, )
    renderer_classes = (ArticleJSONRenderer, )
    pagination_class = ArticlePageNumberPagination

    def create(self, request, **kwargs):
        data = {}
        data["title"] = request.data.get("title")
        data["description"] = request.data.get("description")
        data["body"] = request.data.get("body")
        data["tagList"] = request.data.get("tagList")
        ArticleTagView.create_tag(ArticleTagView, request.data.get("tagList"))
        serializer = ArticleSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        save_serialiser = serializer.save(
            author=self.request.user
        )
        for tag in data['tagList']:
            save_serialiser.tagList.add(
                ArticleTag.objects.get(article_tag_text=tag))
        return Response({"article": serializer.data}, status=status.HTTP_201_CREATED)


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

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        tags = request.data.get("tagList")
        tag = ArticleTagView.create_tag(
            ArticleTagView, request.data.get("tagList"))
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if not tags:
            instance.tagList.clear()
        for tag in tags:
            get_tag = ArticleTag.objects.all()
            for remove_tag in get_tag:
                if str(remove_tag) not in tags:
                    instance.tagList.remove(remove_tag)
            instance.tagList.add(
                ArticleTag.objects.get(article_tag_text=tag))
        return Response(serializer.data)

    def destroy(self, request, pk, **kwargs):
        user = request.user
        queryset = Article.objects.all().filter(id=pk)
        if queryset:
            if queryset[0].author == user:
                self.perform_destroy(queryset)
                return Response("You have succesfully deleted the article")
            return Response("You do not have permision to delete the article")
        return Response(self.err_message, status=status.HTTP_404_NOT_FOUND)
