from decimal import Decimal
from rest_framework import serializers
from django.db import transaction
from src.apps.wallet.models import Wallet, Currency

class WalletCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = [
            "id",
            "wallet_number",
            "user",
            "balance",
            "currency",
            "expired_date",
            "is_active",
        ]
        read_only_fields = ["id", "wallet_number", "expired_date", "balance", "is_active"]

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user

        currency = validated_data.get("currency")
        if not currency:
            # Adjust if your Currency model uses code instead of name
            currency, _ = Currency.objects.get_or_create(name="UZS")

        with transaction.atomic():
            # Do NOT call .objects.create() here
            wallet = Wallet(
                user=user,
                currency=currency,
                balance=Decimal("0.00"),
                is_active=False,
            )
            # This sets wallet_number + expired_date and performs the FIRST save
            wallet.generate_card()

        return wallet
