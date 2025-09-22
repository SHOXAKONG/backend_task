from rest_framework import serializers
from src.apps.users.models import User


class AuthForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError('This email does not exist')
        return value