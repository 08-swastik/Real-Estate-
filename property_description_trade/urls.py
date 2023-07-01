from django.urls import path
from . import views

app_name = 'property_description_trade'

urlpatterns = [
    path('property/<int:property_id>/', views.property_detail, name='property_detail'),
    path('property/<int:property_id>/payment/', views.payment, name='payment'),
    path('property/<int:property_id>/payment/confirmation/<str:billing_name>/', views.confirmation, name='confirmation'),
]



