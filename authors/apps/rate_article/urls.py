from django.urls import path
from .views import CreateArticleRating


urlpatterns = [
    path('articles/<article_id>/rating/',
         CreateArticleRating.as_view(), name='rating')
]
