from rest_framework import serializers
from src.apps.wallet.models import Currency


class CurrencySerializer(serializers.ModelSerializer):
    id = serializers.CharField(write_only=True)

    class Meta:
        model = Currency
        fields = [
            'id',
            'name'
        ]