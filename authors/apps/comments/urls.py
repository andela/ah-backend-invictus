from django.urls import path
from .views import ListCreateComment, RetrieveUpdateDeleteComment


urlpatterns = [
    path('articles/<article_id>/comments/', ListCreateComment.as_view(),
         name="comment_list"),
    path('articles/<article_id>/comments/<int:pk>/',
         RetrieveUpdateDeleteComment.as_view(), name="comment_detail")
]
