from django.urls import path
from .views import CreateBookmark, ListBookmarks, RetrieveBookmark, DeleteBookmark


urlpatterns = [
    path('articles/<int:pk>/bookmarks/',
         CreateBookmark.as_view(), name="create_bookmarks"),
    path('bookmarks/', ListBookmarks.as_view(), name="list_bookmarks" ),
    path('bookmarks/<int:pk>/', RetrieveBookmark.as_view(), name="retrieve_bookmark" ),
    path('bookmarks/<int:pk>/delete/', DeleteBookmark.as_view(), name="delete_bookmark" )
]
