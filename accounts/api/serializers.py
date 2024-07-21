from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class CustomSerializer(serializers.Serializer):
    """
    Handles user login and JWT token generation.

    Fields:
    - username: User's username.
    - password: User's password.

    Method:
    - validate: Authenticates user and returns JWT tokens if valid.
    Raises validation error if credentials are incorrect.
    """

    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError(
                "Invalid data. Username or password incorrect"
            )

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return {
            "refresh": str(refresh),
            "access": access_token,
            "username": user.username,
        }
