from calendar import monthrange
from datetime import date
from rest_framework import serializers
from src.apps.card.models import Card


class CardCreateSerializer(serializers.ModelSerializer):
    expired_date = serializers.CharField()

    class Meta:
        model = Card
        fields = ['card_number', 'expired_date', 'user']
        read_only_fields = ['user']


    def validate_expired_date(self, value):
        try:
            month, year = value.split('/')
            month = int(month)
            year = int('20' + year) if len(year) == 2 else int(year)

            if not 1 <= month <= 12:
                raise ValueError

            last_day = monthrange(year, month)[1]
            return date(year, month, last_day)
        except Exception:
            raise serializers.ValidationError("Invalid format. Use MM/YY (e.g. 09/29).")

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)
