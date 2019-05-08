import uuid

from rest_framework.response import Response
from rest_framework import status

from .models import User


class SocialLoginSignUp:
    """
    This class logs in or registers a new social user.
    """

    def social_signup(self, user_info, **kwargs):
        """
        If user exists, authenticate user with their `social account` info.
        If user does not exist, register user using their `social accounts`
        info.
        Returns: `user details` and an `access token`.
        """
        try:
            # Authenticate user with email address.
            user = User.objects.get(email=user_info.get('email'))
            user_dict = {
                "email": user.email
            }
            token = user.encode_auth_token(user_dict)
            password = User.objects.make_random_password()
            return Response({
                "email": user.email,
                "username": user.username,
                "token": token,
                "message": "Successfully logged in."
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            # Create user if user does not exist.
            user_dict = {
                "email": user_info.get("email")
            }
            password = User.objects.make_random_password()
            user = User(
                username=user_info.get('name')+str(uuid.uuid1().int)[:3],
                email=user_info.get('email'),
                is_active=True,
                email_verified=True
            )
            user.set_password(password)
            user.save()
            token = user.encode_auth_token(user_dict)
            return Response({
                "email": user.email,
                "username": user.username,
                "token": token,
                "message": "Account successfully created."
            }, status=status.HTTP_201_CREATED)
