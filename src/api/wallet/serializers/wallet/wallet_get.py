from rest_framework import serializers

from src.api.users.serializers import UserSerializer
from src.apps.wallet.models import Wallet
from ..currency.currency_get import CurrencySerializer


class WalletGetSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    user = UserSerializer()
    currency = CurrencySerializer()

    class Meta:
        model = Wallet
        fields = [
            "id",
            "wallet_number",
            "user",
            "balance",
            "currency",
            "is_active"
        ]

