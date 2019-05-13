from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from .serializers import FetchUserProfileSerializer, UpdateProfileSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import NotFound
from .renderers import ProfileJSONRenderer
from .models import UserProfile, Follow
from .models import User
from .models import UserProfile


class UserProfiles(ListAPIView):

    permission_classes = (AllowAny, IsAuthenticated)
    queryset = UserProfile.objects.all()
    serializer_class = FetchUserProfileSerializer

    def list(self, request, format=None):
        """
        Return a list of user profiles.
        """
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response({"profiles": serializer.data},
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
                                               data=request.data['profile'],
                                               context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save(data=request.data)
            return Response(serializer.data)
        return Response(
            data={'message':
                   'You have no permissions to edit others profile.'},
            status=status.HTTP_403_FORBIDDEN
        )

def get_user_object(username):
    # get user object
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        raise NotFound(detail='User not found.')


class FollowView(APIView):
    #Function to handle follow user functionality
    permission_classes = (IsAuthenticated,)

    def get_follow_object(self, follower, followed):
        # Method to get a follow object
        try:
            return Follow.objects.get(follower=follower, followed=followed)
        except Follow.DoesNotExist:
            return None

    def post(self, request, username):
        # post to follow a user
        user = get_user_object(username)
        if user == request.user:
            return Response({'error': 'Sorry, you can not follow your self.'},
                            status=status.HTTP_400_BAD_REQUEST)
        if not self.get_follow_object(request.user, user):
            Follow(followed=user, follower=request.user).save()
        message = f"You are following {user.username}."
        return Response({'message': message}, status=status.HTTP_200_OK,)

    def delete(self, request, username):
        # unfollow a user
        user = get_user_object(username)
        follow_Obj = self.get_follow_object(request.user, user)
        if not follow_Obj:
            return Response({'error': f'You are not following {user.username}.'},
                            status=status.HTTP_400_BAD_REQUEST)
        follow_Obj.delete()
        message = f"You have successfully unfollowed {user.username}."
        return Response({'message': message}, status=status.HTTP_200_OK,)


class Followers(APIView):
    """ Return users that follow the provided username"""
    permission_classes = (IsAuthenticated,)

    def get(self, request, username):
        # get the user's followers
        user = get_user_object(username)
        followers = Follow.objects.filter(followed=user)
        profiles = []
        for value in followers:
            profile = FetchUserProfileSerializer(UserProfile.objects.get(user=value.follower))
            profiles.append(profile.data)
        if not profiles:
            profiles = {"message": "No followers for "+username}
        return Response(profiles, status=status.HTTP_200_OK,)


class Following(APIView):
    """ Return users that the provided username follows"""
    permission_classes = (IsAuthenticated,)

    def get(self, request, username):
        # get users this user follows
        user = get_user_object(username)
        followings = Follow.objects.filter(follower=user)
        profiles = []
        for value in followings:
            profile = FetchUserProfileSerializer(UserProfile.objects.get(user=value.followed))
            profiles.append(profile.data)
        if not profiles:
            profiles = {"message": username+" is not following any users"}
        return Response(profiles, status=status.HTTP_200_OK,)
