from django.urls import path
from .views import FavoriteView, FavoritesView
urlpatterns = [
    path('favorites/', FavoritesView.as_view(), name='favorites'),
    path('<int:article_id>/favorites/', FavoriteView.as_view(),
         name='favorite'),
]
