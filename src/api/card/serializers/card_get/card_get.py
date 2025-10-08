from rest_framework import serializers

from src.api.wallet.serializers import CurrencySerializer
from src.apps.card.models import Card
from src.api.users.serializers.users import UserSerializer


class CardGetSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    user = UserSerializer()
    currency = CurrencySerializer()

    class Meta:
        model = Card
        fields = [
            'id',
            'user',
            'card_number',
            'expired_date',
            'balance',
            'created_at',
            "is_active",
            "currency"
        ]
