from django.urls import path
from .views import RetrieveUpdateDestroyArticle, Like, Dislike,\
    ListArticles, CreateArticles, Reports, ReportView


urlpatterns = [
    path('articles/', CreateArticles.as_view(),
         name="articles-list-create"),
    path('articles/all/', ListArticles.as_view(), name="list_articles"),
    path('articles/<int:pk>/', RetrieveUpdateDestroyArticle.as_view(),
         name="article-get-update-delete"),
    path('articles/<article_id>/like/', Like.as_view(), name="like-article"),
    path('articles/<article_id>/dislike/',
         Dislike.as_view(), name="dislike-article"),
    path('articles/<article_id>/report/',
         Reports.as_view(), name="report-article"),
    path('articles/reports/', ReportView.as_view(), name="view-reports"),
]
