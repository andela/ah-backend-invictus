from django.urls import path
from .views import UserProfiles, Updateprofile

urlpatterns = [
    path('users/profiles/', UserProfiles.as_view(), name="get_profile"),
    path('users/profile/<str:username>/', Updateprofile.as_view(), name="update_profile")
]
