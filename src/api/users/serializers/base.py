from rest_framework import serializers
from src.apps.users.models import User


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'password',
            'is_active',
            'is_staff',
        ]

        extra_kwargs = {
            "id": {"read_only": True},
            "is_active": {"read_only": True},
            "is_staff": {"read_only": True},
            "password": {"write_only": True},
        }
