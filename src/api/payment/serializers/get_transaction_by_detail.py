from rest_framework import serializers

from src.api.card.serializers import CardGetSerializer
from src.api.wallet.serializers import WalletGetSerializer, CurrencySerializer
from src.apps.payment.models import Transaction


class GetDetailTransactionSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    sender_wallet = WalletGetSerializer()
    receiver_wallet = WalletGetSerializer()
    sender_card = CardGetSerializer()
    receiver_card = CardGetSerializer()
    currency = CurrencySerializer()

    class Meta:
        model = Transaction
        fields = [
            'id',
            'sender_wallet',
            'receiver_wallet',
            'sender_card',
            'receiver_card',
            'currency',
            'created_at',
            'description',
            'status',
        ]
