from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers
from django.utils import timezone
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from src.apps.wallet.models import Wallet
from src.apps.users.models import Code


@extend_schema_serializer(component_name="WalletConfirmCode")
class ConfirmCodeSerializer(serializers.Serializer):
    code = serializers.CharField(write_only=True)

    def validate_code(self, value: str) -> str:
        request = self.context.get("request")
        if not request or not getattr(request.user, "is_authenticated", False):
            raise serializers.ValidationError("Authentication required")

        try:
            code_obj = Code.objects.get(code=value, user=request.user)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Code is not correct")

        if code_obj.expired_time <= timezone.now():
            raise serializers.ValidationError("Code has expired")

        return value

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user
        value = validated_data["code"]

        with transaction.atomic():
            try:
                code_obj = (
                    Code.objects
                    .select_for_update()
                    .get(code=value, user=user)
                )
            except ObjectDoesNotExist:
                raise serializers.ValidationError({"code": "Code is not correct"})

            if code_obj.expired_time <= timezone.now():
                raise serializers.ValidationError({"code": "Code has expired"})

            wallet = (
                Wallet.objects
                .select_for_update()
                .filter(user=user, is_active=False)
                .order_by("-created_at")
                .first()
            )
            if wallet is None:
                raise serializers.ValidationError({"code": "No inactive wallet to activate"})

            if not wallet.is_active:
                wallet.is_active = True
                wallet.save(update_fields=["is_active"])

            # Consume the code so it can’t be reused
            code_obj.delete()

        return wallet
