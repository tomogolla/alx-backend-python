from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer to add extra claims
    to the JWT access token payload upon login
    and update is_online in model.
    """

    def validate(self, attrs):
        data = super().validate(attrs)

        # Check if user was successfully authenticated
        if self.user:
            # Update the is_online field
            self.user.is_online = True
            self.user.save(update_fields=['is_online'])
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Adds custom claims
        token['email'] = user.email
        token['username'] = user.username

        return token