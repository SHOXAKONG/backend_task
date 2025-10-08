from ..models import Card
from django.contrib import admin

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    pass