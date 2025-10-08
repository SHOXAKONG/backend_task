from rest_framework import serializers
from django.db import transaction as db_transaction
from src.apps.card.models import Card
from src.apps.payment.models import Transaction
from src.apps.payment.models.status import Status
from src.apps.wallet.models import Wallet


class TransactionCardToWalletSerializer(serializers.ModelSerializer):
    sender_card_number = serializers.CharField(write_only=True)
    receiver_wallet_number = serializers.CharField(write_only=True)

    class Meta:
        model = Transaction
        fields = [
            'sender_card_number',
            'receiver_wallet_number',
            'amount',
            'description',
        ]

    def validate(self, attrs):
        sender_card_number = attrs.get("sender_card_number")
        receiver_wallet_number = attrs.get("receiver_wallet_number")
        amount = attrs.get("amount")

        try:
            sender_card = Card.objects.get(card_number=sender_card_number)
        except Card.DoesNotExist:
            raise serializers.ValidationError("Sender card not found.")

        try:
            receiver_wallet = Wallet.objects.get(wallet_number=receiver_wallet_number)
        except Wallet.DoesNotExist:
            raise serializers.ValidationError("Receiver wallet not found.")

        if amount <= 0:
            raise serializers.ValidationError("Transfer amount must be greater than zero.")

        if sender_card.balance < amount:
            raise serializers.ValidationError("Insufficient balance on sender card.")

        if not sender_card.is_active:
            raise serializers.ValidationError("Sender card is not active.")
        if not receiver_wallet.is_active:
            raise serializers.ValidationError("Receiver wallet is not active.")

        attrs["sender_card"] = sender_card
        attrs["receiver_wallet"] = receiver_wallet
        return attrs

    def create(self, validated_data):
        sender_card = validated_data["sender_card"]
        receiver_wallet = validated_data["receiver_wallet"]
        amount = validated_data["amount"]

        with db_transaction.atomic():
            sender_card.balance -= amount
            receiver_wallet.balance += amount
            sender_card.save(update_fields=["balance"])
            receiver_wallet.save(update_fields=["balance"])

            transaction = Transaction.objects.create(
                sender_card=sender_card,
                receiver_wallet=receiver_wallet,
                amount=amount,
                status=Status.PENDING[0],
                currency=sender_card.currency,
                description=validated_data.get("description", ""),
            )

        return transaction
