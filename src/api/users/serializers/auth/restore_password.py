from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from ..base import BaseUserSerializer


class RestorePasswordSerializer(BaseUserSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta(BaseUserSerializer.Meta):
        fields = tuple(BaseUserSerializer.Meta.fields) + ("password_confirm",)
        extra_kwargs = {
            **BaseUserSerializer.Meta.extra_kwargs,
            "first_name": {"read_only": True},
            "last_name": {"read_only": True},
            "email": {"read_only": True},
            "password_confirm": {"write_only": True},
        }

    def validate(self, data):
        if data.get("password") != data.get("password_confirm"):
            raise serializers.ValidationError({"password": "Passwords do not match"})
        try:
            validate_password(data.get("password"))
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        return data

    def save(self, **kwargs):
        user = kwargs.get("user")
        if not user:
            raise serializers.ValidationError("User not found.")

        user.set_password(self.validated_data["password"])
        user.save()
        return user
