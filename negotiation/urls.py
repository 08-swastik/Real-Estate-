from django.urls import path
from . import views


app_name = 'negotiation'
urlpatterns = [
    path('negotiate/<int:property_id>/', views.negotiation_form, name='negotiation_form'),  
    path('property/<int:property_id>/available_negotiations',views.available_negotiations, name = 'available_negotiations'),
    path('myoffers/',views.my_offers, name = 'my_offers'),
    path('my_negotiations/',views.my_negotiations, name = 'my_negotiations'),
    path('reject_offer/<int:negotiation_id>/',views.delete_offers,name = "delete_offers")
    
]
