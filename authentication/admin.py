from django.contrib import admin
from .models import Seller

class SellerAdmin(admin.ModelAdmin):
    list_display = ('username','first_name', 'last_name', 'email', 'phone_number', 'address')

admin.site.register(Seller,SellerAdmin)
# Register your models here.

# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.models import User

# from .models import Seller

# class CustomUserAdmin(UserAdmin):
#     list_display = ('username', 'first_name', 'last_name', 'email', 'seller_address', 'seller_phone_number')

#     def seller_address(self, obj):
#         return obj.seller.address
    
#     def seller_phone_number(self, obj):
#         return obj.seller.phone_number

# admin.site.unregister(User)
# admin.site.register(User, CustomUserAdmin)
# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.models import User



# class CustomUserAdmin(UserAdmin):
#     list_display = ('username', 'first_name', 'last_name', 'email', 'address', 'phone_number')

#     def address(self, obj):
#         return obj.address
    
#     def phone_number(self, obj):
#         return obj.phone_number

# admin.site.unregister(User)
# admin.site.register(User, CustomUserAdmin)

# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.models import User
# from .models import Seller

# class CustomUserAdmin(UserAdmin):
#     list_display = ('username', 'first_name', 'last_name', 'email', 'get_address', 'get_phone_number')

#     def get_address(self, obj):
#         seller = Seller.objects.get(user=obj)
#         return seller.address

#     def get_phone_number(self, obj):
#         seller = Seller.objects.get(user=obj)
#         return seller.phone_number

# admin.site.unregister(User)
# admin.site.register(User, CustomUserAdmin)



