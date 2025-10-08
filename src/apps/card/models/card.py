from calendar import monthrange
from datetime import date

from django.core.exceptions import ValidationError
from django.db import models
from src.apps.common.models import BaseModel
from src.apps.users.models import User
import uuid

from src.apps.wallet.models import Currency


class Card(BaseModel):
    id = models.CharField(default=uuid.uuid4, editable=False, primary_key=True)
    card_number = models.CharField(max_length=16, unique=True, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expired_date = models.DateField()
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=False)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, default='091f557f-53bd-4a38-af7d-7f7fe71a86e3')

    class Meta:
        db_table = 'card'

    def clean(self):
        if not self.card_number.isdigit():
            raise ValidationError({"card_number": "Card number must be digit"})
        if len(self.card_number) != 16:
            raise ValidationError({"card_number": "Card number should be 16"})
        if self.balance < 0:
            raise ValidationError({"balance": "Balance Can not be negative"})

    def save(self, *args, **kwargs):
        if isinstance(self.expired_date, str):
            try:
                month, year = self.expired_date.split('/')
                month = int(month)
                year = int('20' + year) if len(year) == 2 else int(year)
                if not 1 <= month <= 12:
                    raise ValueError

                last_day = monthrange(year, month)[1]
                self.expired_date = date(year, month, last_day)
            except Exception:
                raise ValidationError(
                    {"expired_date": "Invalid format. Use MM/YY (e.g. '09/29')."}
                )

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.card_number} - {self.is_active}"
