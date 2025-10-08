from django.db import models
import uuid

from src.apps.card.models import Card
from src.apps.common.models import BaseModel
from src.apps.wallet.models import Wallet, Currency
from .status import Status


class Transaction(BaseModel):
    id = models.CharField(default=uuid.uuid4, editable=False, primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)

    sender_wallet = models.ForeignKey(
        Wallet,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sent_transactions_wallet'
    )
    receiver_wallet = models.ForeignKey(
        Wallet,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='received_transactions_wallet'
    )

    sender_card = models.ForeignKey(
        Card,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sent_transactions_card'
    )
    receiver_card = models.ForeignKey(
        Card,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='received_transactions_card'
    )

    status = models.CharField(choices=Status.choices, max_length=30, db_index=True)
    currency = models.ForeignKey(
        Currency,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'transaction'
