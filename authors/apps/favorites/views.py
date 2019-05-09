from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from authors.apps.articles.models import Article
from authors.apps.articles.serializers import ArticleSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from .models import Favorites


class FavoriteView(APIView):
    #Function to handle favorite articles functionality
    permission_classes = (IsAuthenticated,)

    def get_article_object(self, pk):
        # Method to get an articles by Id
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            raise NotFound(detail='Article not found.')

    def get_favorite_object(self, article_id, user_id):
        # returns favorite object if exists or returns None
        try:
            return Favorites.objects.get(article=article_id, user=user_id)
        except Favorites.DoesNotExist:
            return None

    def get(self, request, article_id):
        # toggle aticle as favorite or not favorite
        article = self.get_article_object(article_id)
        favorite = self.get_favorite_object(article_id, request.user.id)
        favs_count = None
        favorited = article.favorited
        message = None
        if favorite:
            favorite.delete()
            favs_count = article.favorite_count - 1
            message = "Article removed from favorites."
            if favs_count < 1:
                favorited = False
        elif not article.author.id == request.user.id:
            # Check that request is not from the article author
            favorite = Favorites(article=article, user=request.user)
            favorite.save()
            favs_count = article.favorite_count + 1
            favorited = True
            message = "Article added to favorites."
        else:
            return Response(
                {'error': "You can not favorite your own article!"
                },status=status.HTTP_400_BAD_REQUEST,)
        Article.objects.filter(id=article_id).update(favorite_count=favs_count,
                                                     favorited=favorited)
        return Response({'message': message}, status=status.HTTP_200_OK,)


class FavoritesView(APIView):
    """ Return favorite articles """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # get user's favorite articles
        favs = Favorites.objects.filter(user=request.user)
        fav_articles = []
        for fav in favs:
            article = Article.objects.get(pk=fav.article.pk)
            article = ArticleSerializer(article, many=False,
                                        context={'request': request})
            fav_articles.append(article.data)
        return Response(fav_articles,status=status.HTTP_200_OK,)
