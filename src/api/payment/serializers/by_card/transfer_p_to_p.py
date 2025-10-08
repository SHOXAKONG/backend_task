from rest_framework import serializers
from django.db import transaction as db_transaction
from src.apps.payment.models import Transaction
from src.apps.payment.models.status import Status
from src.apps.card.models import Card


class TransferByCardPToP(serializers.ModelSerializer):
    sender_card_number = serializers.CharField(write_only=True)
    receiver_card_number = serializers.CharField(write_only=True)

    class Meta:
        model = Transaction
        fields = [
            'sender_card_number',
            'receiver_card_number',
            'amount',
            'description',
        ]

    def validate(self, attrs):
        sender_card_number = attrs.get("sender_card_number")
        receiver_card_number = attrs.get("receiver_card_number")
        amount = attrs.get("amount")

        try:
            sender_card = Card.objects.get(card_number=sender_card_number)
        except Card.DoesNotExist:
            raise serializers.ValidationError("Sender card not found.")

        try:
            receiver_card = Card.objects.get(card_number=receiver_card_number)
        except Card.DoesNotExist:
            raise serializers.ValidationError("Receiver card not found.")

        if sender_card == receiver_card:
            raise serializers.ValidationError("Sender and receiver cards cannot be the same.")

        if amount <= 0:
            raise serializers.ValidationError("Transfer amount must be greater than zero.")

        if sender_card.balance < amount:
            raise serializers.ValidationError("Insufficient balance on sender card.")

        if not sender_card.is_active:
            raise serializers.ValidationError("Sender card is not active.")
        if not receiver_card.is_active:
            raise serializers.ValidationError("Receiver card is not active.")

        attrs["sender_card"] = sender_card
        attrs["receiver_card"] = receiver_card
        return attrs

    def create(self, validated_data):
        sender_card = validated_data["sender_card"]
        receiver_card = validated_data["receiver_card"]
        amount = validated_data["amount"]

        with db_transaction.atomic():
            sender_card.balance -= amount
            receiver_card.balance += amount

            sender_card.save(update_fields=["balance"])
            receiver_card.save(update_fields=["balance"])

            transaction = Transaction.objects.create(
                sender_card=sender_card,
                receiver_card=receiver_card,
                amount=amount,
                status=Status.PENDING[0],
                currency=sender_card.currency,
                description=validated_data.get("description", ""),
            )

        return transaction
