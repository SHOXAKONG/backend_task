from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from src.apps.users.models import User


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(write_only=True)

    def validate(self, data):
        refresh_token = data['refresh_token']

        refresh = RefreshToken(refresh_token)
        if not refresh:
            return serializers.ValidationError("Invalid or expired refresh token.")

        user_id = refresh['user_id']
        user = User.objects.get(id=user_id)
        if not user:
            return serializers.ValidationError("No active user")

        new_refresh = RefreshToken.for_user(user)
        new_access = new_refresh.access_token

        return {
            "refresh": str(new_refresh),
            "access": str(new_access)
        }
