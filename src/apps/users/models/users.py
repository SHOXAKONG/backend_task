import uuid
from .user_manager import UserManager
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=200, null=True, blank=True)

    objects = UserManager()

    REQUIRED_FIELDS = ["first_name", "last_name"]
    USERNAME_FIELD = "email"

    def __str__(self):
        return f"Full Name: {self.first_name} {self.last_name}"

    class Meta:
        db_table = "user"
