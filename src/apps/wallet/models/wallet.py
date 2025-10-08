from django.db import models, transaction, IntegrityError
from ..utils import generate_luhn_number, default_expired_date
from src.apps.common.models import BaseModel
import uuid
from src.apps.users.models import User
from .currency import Currency


class Wallet(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wallet_number = models.CharField(max_length=16, unique=True, db_index=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    expired_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = 'wallet'

    def __str__(self):
        return f"{self.user} - {self.balance} - {self.currency}"

    def generate_card(self, prefix='4000', length=16, max_tries=50):
        if self.wallet_number:
            return self.wallet_number, self.expired_date

        tries = 0
        while tries < max_tries:
            try:
                with transaction.atomic():
                    candidate = generate_luhn_number(prefix, length)
                    if Wallet.objects.filter(wallet_number=candidate).exists():
                        tries += 1
                        continue
                    self.wallet_number = candidate
                    self.expired_date = default_expired_date(years=5)
                    self.save(update_fields=['wallet_number', 'expired_date'])
                    return self.wallet_number, self.expired_date
            except IntegrityError:
                tries += 1
                continue
        raise RuntimeError("Card number generation failed after retries.")

