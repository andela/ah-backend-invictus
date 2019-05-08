from django.utils import timezone

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from authors.apps.article_tags.views import ArticleTagView
from authors.apps.article_tags.models import ArticleTag
from .article_filter import ArticleFilter
from .renderer import ArticleJSONRenderer
from .models import Article, Like_Dislike
from .serializers import ArticleSerializer
from .permissions import IsOwnerOrReadOnly
from .pagination import ArticlePageNumberPagination


class ListArticles(generics.ListAPIView):
    """ Get articles"""
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    authentication_classes = ()
    renderer_classes = (ArticleJSONRenderer, )
    pagination_class = ArticlePageNumberPagination

    filter_class = ArticleFilter
    filter_backends = (SearchFilter, DjangoFilterBackend, )
    search_fields = ('title', 'author__username', 'description')


class CreateArticles(generics.CreateAPIView):
    """
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


class Like(APIView):
    """
    POST articles/:id/like/ to like an article
    GET articles/:id/ and view likes_count
    """
    permission_classes = (IsAuthenticated, )

    def get_article(self, article_id):
        """ Method to search for an article object by its id"""
        try:
            return Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            raise NotFound({"error": "Article does not exist"})

    def post(self, request, **kwargs):
        """ Method to like an article and if endpoint hit twice
            by same user for that article revoke like
        """

        article = self.get_article(kwargs['article_id'])

        my_choice = Like_Dislike.objects.filter(
            article_id=kwargs['article_id'], reviewer_id=request.user.username)
        my_choice_reset = Like_Dislike.objects.filter(
            article_id=kwargs['article_id'], reviewer_id=request.user.username, like_or_dislike=0)
        my_like_already = Like_Dislike.objects.filter(
            article_id=kwargs['article_id'], reviewer_id=request.user.username, like_or_dislike=1)
        my_dislike_already = Like_Dislike.objects.filter(
            article_id=kwargs['article_id'], reviewer_id=request.user.username, like_or_dislike=-1)

        if not my_choice:
            like = Like_Dislike(
                reviewer=request.user, like_or_dislike=1, article=article
            )
            like.save()
            Article.objects.filter(
                id=kwargs['article_id']).update(
                likes_count=article.likes_count + 1)
            return Response({"success": "You have successfully liked this article."})
        else:
            if my_choice_reset:
                Like_Dislike.objects.filter(
                    article_id=kwargs['article_id'], reviewer_id=request.user.username).update(like_or_dislike=1)                
                Article.objects.filter(
                    id=kwargs['article_id']).update(
                    likes_count=article.likes_count + 1)
                return Response({"success": "You have successfully liked this article."})
            elif my_like_already:
                # my_choice.delete()
                Like_Dislike.objects.filter(
                    article_id=kwargs['article_id'], reviewer_id=request.user.username).update(like_or_dislike=0)
                Article.objects.filter(
                    id=kwargs['article_id']).update(likes_count=article.likes_count - 1)
                return Response(
                    {"message": "Your like has been revoked"}, status=status.HTTP_200_OK,)
            elif my_dislike_already:
                Like_Dislike.objects.filter(
                    article_id=kwargs['article_id'], reviewer_id=request.user.username).update(like_or_dislike=1)
                Article.objects.filter(
                    id=kwargs['article_id']).update(
                        likes_count=article.likes_count + 1, dislikes_count=article.dislikes_count - 1)
                return Response({"success": "Your dislike for the article has changed to a like."})


class Dislike(APIView):
    """
    POST articles/:id/dislike/ to dislike an article
    GET articles/:id/ and view dislikes_count
    """
    permission_classes = (IsAuthenticated, )

    def get_article(self, article_id):
        """ Method to search for an article object by its id"""
        try:
            return Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            raise NotFound({"error": "Article does not exist"})

    def post(self, request, **kwargs):
        """ Method to dislike an article and if endpoint hit twice
            by same user for that article revoke dislike
        """
        article = self.get_article(kwargs['article_id'])
        my_choice = Like_Dislike.objects.filter(
            article_id=kwargs['article_id'], reviewer_id=request.user.username)
        my_choice_reset = Like_Dislike.objects.filter(
            article_id=kwargs['article_id'], reviewer_id=request.user.username, like_or_dislike=0)
        my_dislike_already = Like_Dislike.objects.filter(
            article_id=kwargs['article_id'], reviewer_id=request.user.username, like_or_dislike=-1)
        my_like_already = Like_Dislike.objects.filter(
            article_id=kwargs['article_id'], reviewer_id=request.user.username, like_or_dislike=1)

        if not my_choice:
            # if I have never liked or disliked or reset my choice to 0
            dislike = Like_Dislike(
                reviewer=request.user, like_or_dislike=-1, article=article)
            dislike.save()
            Article.objects.filter(
                id=kwargs['article_id']).update(
                    dislikes_count=article.dislikes_count + 1)

            return Response({"success": "You have successfully disliked this article."})

        else:
            if my_choice_reset:
                Like_Dislike.objects.filter(
                    article_id=kwargs['article_id'], reviewer_id=request.user.username).update(like_or_dislike=-1)
                Article.objects.filter(
                    id=kwargs['article_id']).update(
                        dislikes_count=article.dislikes_count + 1)
                return Response({"success": "You have successfully disliked this article."})
            # check if there was a previous choice. Either the person had disliked or liked before
            elif my_dislike_already:
                # my_choice.delete()
                Like_Dislike.objects.filter(
                    article_id=kwargs['article_id'], reviewer_id=request.user.username).update(like_or_dislike=0)
                Article.objects.filter(
                    id=kwargs['article_id']).update(dislikes_count=article.dislikes_count - 1)
                return Response(
                    {"message": "Your dislike has been revoked"}, status=status.HTTP_200_OK,)
            elif my_like_already:
                Like_Dislike.objects.filter(
                    article_id=kwargs['article_id'], reviewer_id=request.user.username).update(like_or_dislike=-1)
                Article.objects.filter(
                    id=kwargs['article_id']).update(
                        likes_count=article.likes_count - 1, dislikes_count=article.dislikes_count + 1)
                return Response({"success": "Your like for the article has changed to a dislike."})
