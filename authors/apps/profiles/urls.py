from django.urls import path
from .views import UserProfiles, Updateprofile, \
     FollowView, Followers, Following

urlpatterns = [
    path('profiles/', UserProfiles.as_view(), name="list_profiles"),
    path('users/profile/<str:username>/', Updateprofile.as_view(),
         name="update_profile"),
    path('profiles/<str:username>/follow/', FollowView.as_view(),
         name="follow"),
    path('profiles/<str:username>/followers/', Followers.as_view(),
         name="getfollowers"),
    path('profiles/<str:username>/following/', Following.as_view(),
         name="getfollowing"),
    path('users/profile/<str:username>/', Updateprofile.as_view(), name="update_profile")
]
