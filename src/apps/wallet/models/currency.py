from django.db import models
import uuid
from src.apps.common.models import BaseModel


class Currency(BaseModel):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=200, db_index=True)

    class Meta:
        db_table = 'currency'
