from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from src.apps.users.models import User
from ..base import BaseUserSerializer

class UserRegisterSerializer(BaseUserSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta(BaseUserSerializer.Meta):
        fields = tuple(BaseUserSerializer.Meta.fields) + ("password_confirm",)
        extra_kwargs = {
            **BaseUserSerializer.Meta.extra_kwargs,
            "password_confirm": {"write_only": True},
        }

    def validate(self, data):
        if data.get("password") != data.get("password_confirm"):
            raise serializers.ValidationError({"password": "Passwords do not match"})
        try:
            validate_password(data.get("password"))
        except DjangoValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')

        user = User.objects.create(
            username=validated_data['email'],
            **validated_data
        )

        user.set_password(password)
        user.save()

        return user
