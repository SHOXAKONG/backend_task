from rest_framework import serializers
from src.apps.users.models import User


class UserListSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            "full_name",
            'email',
            'is_active',
            'is_staff',
            'last_login'
        ]
