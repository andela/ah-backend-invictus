from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import exceptions

from .models import User
from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer
)


class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    authentication_classes = ()
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})
        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Create a unique identifier
        uid = urlsafe_base64_encode(
            force_bytes(user['username'])).decode('utf-8')
        current_site = get_current_site(request)

        activation_link = '{}/api/users/{}/'.format(current_site, uid)

        subject = 'Activate your account'
        message = 'Click the link below to activate your account.\n{}'.format(
            activation_link)
        from_email = settings.EMAIL_HOST_USER
        to_email = user['email']
        send_mail(subject, message, from_email, [to_email],
                  fail_silently=False)

        response_data = {
            'username': user['username'],
            'email': user['email'],
            'message': 'Check your email address to confirm registration.'
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't actually have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        token = User.encode_auth_token(user).decode('utf-8')
        user = User()
        response_data = {
            'username': user.get_full_name,
            'token': token
        }
        response_data.update(serializer.data)
        return Response(
            response_data, status=status.HTTP_200_OK
        )


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class AccountActivationAPIView(APIView):
    """
    Return the registration activation link.
    """
    permission_classes = (AllowAny, )
    authentication_classes = ()
    serializer_class = UserSerializer

    def get(self, request, uid):
        try:
            username = urlsafe_base64_decode(uid).decode('utf-8')
            user = User.objects.filter(username=username).first()
        except User.DoesNotExist:
            message = "User not found."
            return exceptions.AuthenticationFailed(message)
        if user is not None and not user.email_verified:
            user.email_verified = True
            user.save()
            data = {
                "username": user.username,
                "email": user.email
            }
            token = User.encode_auth_token(data).decode('utf-8')
            response = {
                "message": "Account successfully activated. Login now.",
                "token": token
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response({
            "error": "Activation link is invalid.",
        }, status=status.HTTP_400_BAD_REQUEST)
