from django.urls import path
from . import views

app_name = 'property_form'

urlpatterns = [
    path('add_listing',views.seller_register,name="register"),
    
]