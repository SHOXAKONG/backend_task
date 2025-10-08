from rest_framework import serializers

from src.api.card.serializers import CardGetSerializer
from src.api.wallet.serializers import CurrencySerializer, WalletGetSerializer
from src.apps.payment.models import Transaction


class GetTransaction(serializers.ModelSerializer):
    sender_card_number = serializers.CharField(source='sender_card.card_number', read_only=True)
    receiver_card_number = serializers.CharField(source='receiver_card.card_number', read_only=True)
    sender_wallet_number = serializers.CharField(source='sender_wallet.wallet_number', read_only=True)
    receiver_wallet_number = serializers.CharField(source='receiver_wallet.wallet_number', read_only=True)
    # currency = CurrencySerializer()
    # sender_card = CardGetSerializer()
    # receiver_card = CardGetSerializer()
    # receiver_wallet = WalletGetSerializer()
    # sender_wallet = WalletGetSerializer()

    class Meta:
        model = Transaction
        fields = [
            'id',
            'sender_card_number',
            'sender_card',
            'receiver_card_number',
            'receiver_card',
            'receiver_wallet_number',
            'receiver_wallet',
            'sender_wallet_number',
            'sender_wallet',
            'created_at',
            'description',
            'status',
            'amount',
            'currency'
        ]
