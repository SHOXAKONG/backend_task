from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from src.apps.users.models import User


class SetPasswordSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['password', 'password_confirm']

    def validate(self, data):
        password = data['password']
        password_confirm = data['password_confirm']
        if password != password_confirm:
            return serializers.ValidationError("Password Do not Match")
        validate_password(password)
        return data

    def save(self, **kwargs):
        user = kwargs.get("user")
        if not user:
            raise serializers.ValidationError("User not found.")

        user.set_password(self.validated_data["password"])
        user.save()
        return user
