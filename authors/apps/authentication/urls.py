from django.urls import path
from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView,
    AccountActivationAPIView, PasswordReset, PasswordResetToken,
    FacebookAuthenticationAPIView, GoogleAuthenticationAPIView,
    TwitterAuthenticationAPIView
)


urlpatterns = [
     path('user/', UserRetrieveUpdateAPIView.as_view(), name='retrieveupdate'),
     path('users/', RegistrationAPIView.as_view(), name='user_signup'),
     path('users/login/', LoginAPIView.as_view(), name='user_login'),
     path('reset_password/', PasswordReset.as_view(), name='password_reset'),
     path('reset_password/<str:token>/', PasswordResetToken.as_view(),
          name='password_reset_token'),
     path('users/<str:uid>/', AccountActivationAPIView.as_view(),
          name='activation_link'),
     path('social_auth/facebook/', FacebookAuthenticationAPIView.as_view(),
          name='facebook_auth'),
     path('social_auth/google/', GoogleAuthenticationAPIView.as_view(),
          name='google_auth'),
     path('social_auth/twitter/', TwitterAuthenticationAPIView.as_view(),
          name='twitter_auth')
]
