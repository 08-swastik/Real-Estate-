from django.urls import path,include
from . import views


app_name = 'property_description_trade'

urlpatterns = [
    path('property/<int:property_id>/', views.property_detail, name='property_detail'),
     path('checkout/<int:property_id>/', views.checkout, name='checkout'),
    path('success/', views.confirmation, name='confirmation'),
    path('error/', views.error, name='error'),
    path('confirmation/',views.confirmation, name = "confirmation"),
    path('webhook/', views.webhook, name='webhook'),

    # path('paypal/', include('paypal.standard.ipn.urls')),
    # path('success/', views.success , name = 'success' )
    

]



