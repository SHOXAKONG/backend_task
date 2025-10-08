from django.db.models.signals import post_save
from django.dispatch import receiver
from src.apps.payment.models import Transaction
from src.apps.payment.models.status import Status


@receiver(post_save, sender=Transaction)
def update_transaction_status(sender, instance, created, **kwargs):
    if not created:
        return

    try:
        if (
                instance.sender_card
                and instance.receiver_card
                and instance.amount > 0
                and instance.sender_card.is_active
                and instance.receiver_card.is_active
        ):
            instance.status = Status.SUCCESS[0]

        elif (
                instance.sender_wallet
                and instance.receiver_wallet
                and instance.amount > 0
                and instance.sender_wallet.is_active
                and instance.receiver_wallet.is_active
        ):
            instance.status = Status.SUCCESS[0]
        elif (
                instance.sender_wallet
                and instance.receiver_card
                and instance.amount > 0
                and instance.sender_wallet.is_active
                and instance.receiver_card.is_active
        ):
            instance.status = Status.SUCCESS[0]
        elif (
                instance.sender_card
                and instance.receiver_wallet
                and instance.amount > 0
                and instance.sender_card.is_active
                and instance.receiver_card.is_active
        ):
            instance.status = Status.SUCCESS[0]
        else:
            instance.status = Status.FAILED[0]

        instance.save(update_fields=["status"])

    except Exception:
        instance.status = Status.FAILED[0]
        instance.save(update_fields=["status"])
