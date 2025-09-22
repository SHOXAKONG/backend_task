from rest_framework import serializers
from src.apps.users.models import Code, User


class ConfirmCodeSerializer(serializers.Serializer):
    id = serializers.CharField(write_only=True)
    code = serializers.CharField(write_only=True)

    def validate(self, data):
        user_id = data['id']
        code = data['code']
        if not Code.objects.filter(code=code, user=user_id):
            return serializers.ValidationError("Code is not correct")
        return data
