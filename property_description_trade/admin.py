from django.contrib import admin
from .models import ConfirmationData

@admin.register(ConfirmationData)
class ConfirmationDataAdmin(admin.ModelAdmin):
    list_display = ('property', 'email', 'name', 'payment_status', 'amount_total')

# Register your models here.
