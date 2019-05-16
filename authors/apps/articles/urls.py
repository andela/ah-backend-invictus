from django.urls import path
from .views import (UpdateDestroyArticle, RetrieveArticle,
                    Like, Dislike, ListArticles, CreateArticles,
                    Reports, ReportView, AddRead, ReadingStats)


urlpatterns = [
    path('author/readingstats/', ReadingStats.as_view(), name='reading_stats'),
    path('articles/', CreateArticles.as_view(),
         name="articles-list-create"),
    path('articles/all/', ListArticles.as_view(), name="list_articles"),
    path('articles/<int:pk>/', UpdateDestroyArticle.as_view(),
         name="article-update-delete"),
    path('articles/<int:pk>/retrieve/', RetrieveArticle.as_view(),
         name="article-get"),
    path('articles/<article_id>/like/', Like.as_view(), name="like-article"),
    path('articles/<article_id>/dislike/',
         Dislike.as_view(), name="dislike-article"),
    path('articles/<article_id>/report/',
         Reports.as_view(), name="report-article"),
    path('articles/reports/', ReportView.as_view(), name="view-reports"),
    path('articles/reads/', AddRead.as_view(), name="add_user_read"),
]
