from django.contrib import admin
from .models import Seller,Client

class SellerAdmin(admin.ModelAdmin):
    list_display = ('username','first_name', 'last_name', 'email', 'phone_number', 'address')

admin.site.register(Seller,SellerAdmin)


class ClientAdmin(admin.ModelAdmin):
    list_display = ('username','first_name', 'last_name', 'email', 'phone_number', 'address')

admin.site.register(Client,ClientAdmin)
# Register your models here.

