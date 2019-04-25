from django.conf import settings

from rest_framework import authentication, exceptions

from authors.apps.authentication.models import User
import jwt


class JWTAuthentication(authentication.BaseAuthentication):
    """Authenticate requests by using tokens."""

    authentication_header_prefix = "Bearer"

    def authenticate(self, request):
        """Check for authorization header."""
        request.user = None
        header = authentication.get_authorization_header(request).split()
        prefix = self.authentication_header_prefix.lower()
        if not header:
            message = "Token is missing."
            raise exceptions.AuthenticationFailed(message)
        if len(header) == 1 or len(header) > 2:
            message = "Invalid Token, header expects two parameters."
            raise exceptions.AuthenticationFailed(message)
        prefix = header[0].decode('utf-8')
        token = header[1].decode('utf-8')
        if prefix.lower() != 'Bearer'.lower():
            message = "Bearer prefix missing in authorization headers."
            raise exceptions.AuthenticationFailed(message)
        return self.authenticate_credentials(request, token)

    def authenticate_credentials(self, request, token):
        """Identify a user using the token provided."""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, 'utf-8')
        except jwt.ExpiredSignatureError:
            message = "The token has expired, please login again."
            raise exceptions.AuthenticationFailed(message)
        except BaseException:
            message = "The token provided can not be decoded."
            raise exceptions.AuthenticationFailed(message)
        user = User.objects.get(username=payload['sub'])
        if not user:
            message = "User does not exist in the database."
            raise exceptions.AuthenticationFailed(message)
        if not user.is_active:
            message = "User is not activated."
            raise exceptions.AuthenticationFailed(message)
        return (user, token)
