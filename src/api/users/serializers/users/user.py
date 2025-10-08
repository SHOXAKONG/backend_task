from ..base import BaseUserSerializer


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ("id", "first_name", "last_name", "email", "is_active", "is_staff")
