from django.conf import settings
from rest_framework import authentication, exceptions
from authors.apps.authentication.models import User
from rest_framework.response import Response
from rest_framework import status
import jwt


class JWTAuthentication(authentication.BaseAuthentication):
    """Authenticate requests by using tokens."""
    authentication_header_prefix = "Bearer"

    def authenticate(self, request):
        """Check for authorization header."""
        try:
            request.user = None
            header = authentication.get_authorization_header(request).split()
            token = header[1]
            if header[0] != self.authentication_header_prefix:
                message = "Bearer prefix missing in Authorization header"
                return Response(message, status=status.HTTP_401_UNAUTHORIZED)
            return self.authenticate_credentials(request, token)
        except Exception as e:
            raise exceptions.AuthenticationFailed(e)

    def authenticate_credentials(self, request, token):
        """Identify a user using the token provided"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, 'utf-8')
        except BaseException:
            message = "The token provided can not be decoded."
            raise exceptions.AuthenticationFailed(message)
        user = User.objects.get(username=payload['sub']['username'])
        if not user:
            message = "User does not exist in the database."
            raise exceptions.AuthenticationFailed(message)
        if not user.is_active:
            message = "User is not activated."
            raise exceptions.AuthenticationFailed(message)
        return (user, token)

