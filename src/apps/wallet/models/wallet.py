from django.db import models
from src.apps.common.models import BaseModel
import uuid
from src.apps.users.models import User
from .currency import Currency


class Wallet(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)

    class Meta:
        db_table = 'wallet'

    def __str__(self):
        return f"{self.user} - {self.balance}"
