from rest_framework import serializers
from django.db import transaction as db_transaction

from src.apps.card.models import Card
from src.apps.payment.models import Transaction
from src.apps.payment.models.status import Status
from src.apps.wallet.models import Wallet


class TransactionWalletToCardSerializer(serializers.ModelSerializer):
    sender_wallet_number = serializers.CharField(write_only=True)
    receiver_card_number = serializers.CharField(write_only=True)

    class Meta:
        model = Transaction
        fields = [
            'sender_wallet_number',
            'receiver_card_number',
            'amount',
            'description',
        ]

    def validate(self, attrs):
        sender_wallet_number = attrs.get("sender_wallet_number")
        receiver_card_number = attrs.get("receiver_card_number")
        amount = attrs.get("amount")

        try:
            sender_wallet = Wallet.objects.get(wallet_number=sender_wallet_number)
        except Wallet.DoesNotExist:
            raise serializers.ValidationError("Sender wallet not found.")

        try:
            receiver_card = Card.objects.get(card_number=receiver_card_number)
        except Wallet.DoesNotExist:
            raise serializers.ValidationError("Receiver wallet not found.")

        if sender_wallet == receiver_card:
            raise serializers.ValidationError("Sender and receiver wallets cannot be the same.")

        if amount <= 0:
            raise serializers.ValidationError("Transfer amount must be greater than zero.")

        if sender_wallet.balance < amount:
            raise serializers.ValidationError("Insufficient balance on sender wallet.")

        if not sender_wallet.is_active:
            raise serializers.ValidationError("Sender wallet is not active.")
        if not receiver_card.is_active:
            raise serializers.ValidationError("Receiver wallet is not active.")

        attrs["sender_wallet"] = sender_wallet
        attrs["receiver_card"] = receiver_card
        return attrs

    def create(self, validated_data):
        sender_wallet = validated_data["sender_wallet"]
        receiver_card = validated_data["receiver_card"]
        amount = validated_data["amount"]

        with db_transaction.atomic():
            sender_wallet.balance -= amount
            receiver_card.balance += amount

            sender_wallet.save(update_fields=["balance"])
            receiver_card.save(update_fields=["balance"])

            transaction = Transaction.objects.create(
                sender_wallet=sender_wallet,
                receiver_card=receiver_card,
                amount=amount,
                status=Status.PENDING[0],
                currency=sender_wallet.currency,
                description=validated_data.get("description", ""),
            )

        return transaction
