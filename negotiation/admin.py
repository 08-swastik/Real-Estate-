
from django.contrib import admin
from .models import Negotiation

class NegotiationAdmin(admin.ModelAdmin):
    list_display = ('property', 'user','email','first_name','last_name','requested_price','status')
    
    
    

admin.site.register(Negotiation, NegotiationAdmin)




