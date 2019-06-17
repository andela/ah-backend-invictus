from django.urls import path
from .views import CreateArticleRating, GetArticleRating


urlpatterns = [
    path('articles/<article_id>/rating/',
         CreateArticleRating.as_view(), name='rating'),
    path('articles/<article_id>/ratings/',
         GetArticleRating.as_view(), name='ratings')
]
