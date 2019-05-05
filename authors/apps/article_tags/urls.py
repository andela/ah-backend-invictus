from django.urls import path
from .views import ArticleTagView


urlpatterns = [
    path('tags/', ArticleTagView.as_view({'get': 'list'}), name="tags")
]
