from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from src.apps.card.models import Card
from src.apps.users.models import Code


class CardActivateSerializer(serializers.Serializer):
    code = serializers.CharField(write_only=True)

    def validate_code(self, value):
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

            card = (
                Card.objects
                .select_for_update()
                .filter(user=user, is_active=False)
                .order_by("-created_at")
                .first()
            )
            if card is None:
                raise serializers.ValidationError({"code": "No inactive card to activate"})

            if not card.is_active:
                card.is_active = True
                card.save(update_fields=["is_active"])

            code_obj.delete()

        return card