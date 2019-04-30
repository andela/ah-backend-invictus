from django.urls import path
from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView,
    AccountActivationAPIView
)


urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view(), name='retrieveupdate'),
    path('users/', RegistrationAPIView.as_view(), name='user_signup'),
    path('users/login/', LoginAPIView.as_view(), name='user_login'),
    path('users/<str:uid>/', AccountActivationAPIView.as_view(),
         name='activation_link'),
]
