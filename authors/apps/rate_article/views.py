from django.db.models import Avg
from .serializer import RateSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from authors.apps.articles.models import Article
from authors.apps.rate_article.models import Rate


class CreateArticleRating(APIView):
    """
    POST rate/
    list average of article
    """
    serializer_class = RateSerializer
    permission_classes = (IsAuthenticated, )
    queryset = Rate.objects.all()

    def get_object(self, article_id):
        try:
            return Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            raise NotFound("article does not exists")

    def post(self, request, **kwargs):
        """ create article rating"""
        #gets article
        article = self.get_object(self.kwargs['article_id'])
        # checks if author of article doednot rate own article
        if article.author == request.user:
            return Response({"error": "you cannot rate your own article"},
                            status=status.HTTP_403_FORBIDDEN)
        # creates rating
        data = {}
        data['rating'] = request.data.get('rating')
        data['user'] = request.user.username
        serializer = RateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        existing_rate = Rate.objects.all().filter(article_id=article.id,
                                                  user=request.user.username)
        if existing_rate:
            existing_rate.delete()
            self.put(request)
            return Response({"message":
                            "you have successfully updated your rating"}, status=status.HTTP_200_OK)
        else:
            serializer.save(article=article)
            return Response({"rating": serializer.data},
                            status=status.HTTP_201_CREATED)

    def get(self, request, **kwargs):
        """ gets average of a single article rating"""
        article = self.get_object(article_id=kwargs['article_id'])
        queryset = Rate.objects.all().filter(article_id=kwargs['article_id'])
        if queryset.exists():
            article_average = queryset.aggregate(Avg('rating'))
            return Response({"average": {"article rating": article_average.get(
                            'rating__avg'), "article": article.slug}},
                            status=status.HTTP_200_OK)
        return Response({"error": "Rating for article doesnot exists"})

    def put(self, request, **kwargs):
        data = {}
        data['rating'] = request.data.get('rating')
        data['user'] = request.user.username
        article = self.get_object(self.kwargs['article_id'])
        serializer = RateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(article=article)
