from django.contrib.auth import authenticate
from rest_framework import serializers
import re

from .models import User, ResetPasswordToken
from django.contrib.auth.hashers import check_password


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.
    # ensures that password is required and not blank
    # username should not contain trailing and leading white spaces
    email = serializers.EmailField()
    username = serializers.CharField(
        trim_whitespace=True
    )
    password = serializers.CharField(
        max_length=16,
        write_only=True,
        required=True,
        error_messages={
            "required": "Password field is required",
            "blank": "Password field cannot be empty",
        }
    )

    def validate_password(self, password):
        """
            validates that  password is longer than 8 characters
            password is alphanumeric
        """
        if len(password) < 8:
            raise serializers.ValidationError(
                "Password should atleast be 8 characters.")
        if not re.search(r'[0-9]', password) or not re.search(r'[a-zA-Z]', password) or not re.search(r'[!?@#$%^&*.]', password):
            raise serializers.ValidationError(
                "Password should include numbers and alphabets and one special character")
        if re.search(r'[\s]', password):
            raise serializers.ValidationError(
                "Password should not include white spaces")
        return password

    def validate_username(self, username):
        """ validates username"""
        exist_username = User.objects.filter(username=username)
        if exist_username.exists():
            raise serializers.ValidationError(
                "username provided already exists")
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

    def validate_email(self, email):
        """ validates email"""

        exist_email = User.objects.filter(email=email)
        if exist_email.exists():
            raise serializers.ValidationError(
                "email provided already exists")
        return email

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.

    class Meta:
        model = User
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['email', 'username', 'password']

    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new user.
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.
        email = data.get('email', None)
        password = data.get('password', None)

        # As mentioned above, an email is required. Raise an exception if an
        # email is not provided.
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        # As mentioned above, a password is required. Raise an exception if a
        # password is not provided.
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this email/password combination. Notice how
        # we pass `email` as the `username` value. Remember that, in our User
        # model, we set `USERNAME_FIELD` as `email`.
        user = authenticate(username=email, password=password)

        # If no user was found matching this email/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        # Django provides a flag on our `User` model called `is_active`. The
        # purpose of this flag to tell us whether the user has been banned
        # or otherwise deactivated. This will almost never be the case, but
        # it is worth checking for. Raise an exception in this case.
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        # The user not verified flag tells us whether the user accoount is
        # activated after registeration or not. Users should only be able
        # login only if their accounts are activated.
        if not user.email_verified:
            raise serializers.ValidationError(
                'Account not yet activated. Check email for activation link.'
            )

        # The `validate` method should return a dictionary of validated data.
        # This is the data that is passed to the `create` and `update` methods
        # that we will see later on.
        return {
            'email': user.email,
            'username': user.username,

        }


class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""

    # Passwords must be at least 8 characters, but no more than 128
    # characters. These values are the default provided by Django. We could
    # change them, but that would create extra work while introducing no real
    # benefit, so let's just stick with the defaults.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password')

        # The `read_only_fields` option is an alternative for explicitly
        # specifying the field with `read_only=True` like we did for password
        # above. The reason we want to use `read_only_fields` here is because
        # we don't need to specify anything else about the field. For the
        # password field, we needed to specify the `min_length` and
        # `max_length` properties too, but that isn't the case for the token
        # field.

    def update(self, instance, validated_data):
        """Performs an update on a User."""

        # Passwords should not be handled with `setattr`, unlike other fields.
        # This is because Django provides a function that handles hashing and
        # salting passwords, which is important for security. What that means
        # here is that we need to remove the password field from the
        # `validated_data` dictionary before iterating over it.
        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            # For the keys remaining in `validated_data`, we will set them on
            # the current `User` instance one at a time.
            setattr(instance, key, value)

        if password is not None:
            # `.set_password()` is the method mentioned above. It handles all
            # of the security stuff that we shouldn't be concerned with.
            instance.set_password(password)

        # Finally, after everything has been updated, we must explicitly save
        # the model. It's worth pointing out that `.set_password()` does not
        # save the model.
        instance.save()

        return instance


class ResetPasswordTokenSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of ResetPasswordToken class objects."""
    email = serializers.EmailField()

    class Meta:
        model = ResetPasswordToken
        fields = ["email", ]

    def validate(self, data):
        # Validate the email
        email = data.get('email', None)
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to reset password'
            )

        # check that user exists and is active
        user = User.objects.filter(email=email).distinct()
        if not user.exists() or not user.first().is_active:
            raise serializers.ValidationError(
                "No active account with provided email was found.")
        return data


class ResetPasswordSerializer(serializers.ModelSerializer):
    """serialization of user data."""

    password = serializers.CharField(max_length=128,
                                     min_length=8,
                                     write_only=True)

    confirm_password = serializers.CharField(max_length=128,
                                             min_length=8,
                                             write_only=True)

    def validate_password(self, password):
        """
            validates that  password is longer than 8 characters
            password is alphanumeric
        """
        if len(password) < 8:
            raise serializers.ValidationError(
                "Password should atleast be 8 characters.")
        if not re.search(r'[0-9]', password) or not re.search(r'[a-zA-Z]',
                                                              password) or not re.search(r'[!?@#$%^&*.]', password):
            raise serializers.ValidationError(
                "Password should include numbers and alphabets and one special character")
        if re.search(r'[\s]', password):
            raise serializers.ValidationError(
                "Password should not include white spaces")
        return password

    class Meta:
        model = User
        fields = ('password', 'confirm_password')

    def update(self, instance, validated_data):
        """update the User password."""

        password = validated_data.pop('password', None)
        confirm_password = validated_data.pop('confirm_password', None)
        for (key, value) in validated_data.items():
            if key != 'confirm_password':
                setattr(instance, key, value)
        old_password = instance.password
        if password is not None and password == confirm_password:
            instance.set_password(password)
        else:
            raise serializers.ValidationError(
                "Passwords do not match!")
        if check_password(password, old_password):
            raise serializers.ValidationError(
                "New password should be different from previous password.")
        instance.save()
        return instance


class SocialAuthenticationSerializer(serializers.Serializer):
    """
    Serializer class for social authentication requests.
    This handles both facebook and google requests.
    """
    access_token = serializers.CharField(
        required=True, trim_whitespace=True)


class TwitterAuthenticationSerializer(serializers.Serializer):
    """
    Serializer class for twitter authentication requests
    """
    access_token = serializers.CharField(
        required=True, trim_whitespace=True)
    access_token_secret = serializers.CharField(
        required=True, trim_whitespace=True)
