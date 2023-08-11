from django.contrib import admin
from .models import Property

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('address','city','seller','price','status' )

admin.site.register(Property,PropertyAdmin)



# Register your models here.
