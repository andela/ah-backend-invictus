from django.urls import path
from .views import (ListCreateComment, RetrieveUpdateDeleteComment,
                    CommentEditHistoryAPIView, Like)


urlpatterns = [
    path('articles/<article_id>/comments/', ListCreateComment.as_view(),
         name="comment_list"),
    path('articles/<article_id>/comments/<int:pk>/',
         RetrieveUpdateDeleteComment.as_view(), name="comment_detail"),
    path('articles/<article_id>/comments/<int:pk>/like/',
         Like.as_view(), name="like_comment"),
    path('articles/<article_id>/comments/<int:pk>/likes/',
         Like.as_view(), name="get_likes"),
    path('articles/<article_id>/comments/<int:pk>/update_history/',
         CommentEditHistoryAPIView.as_view(), name="update_history")
]
