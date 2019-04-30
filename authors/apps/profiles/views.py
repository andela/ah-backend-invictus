from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from .serializers import FetchUserProfileSerializer, UpdateProfileSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .renderers import ProfileJSONRenderer
from .models import UserProfile
from .models import User


# Create your views here.
class UserProfiles(ListAPIView):

    permission_classes = (AllowAny,)
    queryset = UserProfile.objects.all()
    serializer_class = FetchUserProfileSerializer, UpdateProfileSerializer

    def list(self, request, format=None):
        serializer = self.serializer_class(
            self.get_queryset(),
            many=True
        )
        return Response(data=dict(profiles=serializer.data),
                        status=status.HTTP_200_OK)


class Updateprofile(RetrieveUpdateAPIView):
    permission_classes = (AllowAny, IsAuthenticated)
    queryset = UserProfile.objects.all()
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = UpdateProfileSerializer
    lookup_field = 'username'

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(), user__username=self.kwargs.get('username')
        )

    def put(self, request, *args, **kwargs):
        profile = self.get_object()
        if str(profile) == str(request.user.username):
            serializer = self.serializer_class(profile,
                                           data=request.data['profile'])
            serializer.is_valid(raise_exception=True)
            serializer.save(data=request.data)
            return Response(UpdateProfileSerializer(profile).data)
        return Response(
            data={'message':
                    'You have no permissions to edit others profile.'},
            status=status.HTTP_403_FORBIDDEN
        )

