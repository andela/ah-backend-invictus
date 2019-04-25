from django.urls import path
from .views import ListCreateArticles, RetrieveUpdateDestroyArticle


urlpatterns = [
    path('articles/', ListCreateArticles.as_view(),
         name="articles-list-create"),
    path('articles/<int:pk>/', RetrieveUpdateDestroyArticle.as_view(),
         name="article-get-update-delete"),
]
