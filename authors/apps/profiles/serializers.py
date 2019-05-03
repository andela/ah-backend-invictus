from rest_framework import serializers
from authors.apps.profiles.models import UserProfile
from .models import User
import re


class FetchUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UpdateProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = UserProfile
        fields = (
            'firstname',
            'lastname',
            'username',
            'image',
            'bio'
        )

    def validate_username(self, username):
        username1 =  User.objects.filter(username=username)
        if username1.exists():
            raise serializers.ValidationError("Username already exists")
        if len(username) <= 4:
            raise serializers.ValidationError(
                "username should be longer than 4 characters")
        if re.search(r'[\s]', username):
            raise serializers.ValidationError(
                "username should not contain spaces")
        if not re.search(r'[a-zA-Z]', username):
            raise serializers.ValidationError(
                "username should contain characters")
        return username

    def validate_firstname(self,firstname):
        if len(firstname) <= 3:
            raise serializers.ValidationError(
                "Firstname should be longer than 3 characters")
        return firstname

    def validate_lastname(self,lastname):
        if len(lastname) <= 4:
            raise serializers.ValidationError(
                "Lastname should be longer than 4 characters")
        return lastname


