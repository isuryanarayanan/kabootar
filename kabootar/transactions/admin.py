from django.contrib import admin
from .models import Transaction, TransactionTemplate, SendTransaction

# Register your models here.

class TransactionTemplateInline(admin.TabularInline):
    model = TransactionTemplate

    class Meta:
        ordering = ["priority"]

class TransactionAdmin(admin.ModelAdmin):
    inlines = [TransactionTemplateInline]


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(SendTransaction)