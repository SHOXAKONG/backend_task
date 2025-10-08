from ..models import Code
from django.contrib import admin

@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    pass