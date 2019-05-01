from django.urls import path
from .views import ListCreateArticles, RetrieveUpdateDestroyArticle, Like, Dislike


urlpatterns = [
    path('articles/', ListCreateArticles.as_view(),
         name="articles-list-create"),
    path('articles/<int:pk>/', RetrieveUpdateDestroyArticle.as_view(),
         name="article-get-update-delete"),
     path('articles/<article_id>/like/', Like.as_view(), name="like-article" ),
     path('articles/<article_id>/dislike/', Dislike.as_view(), name="dislike-article" )
]
