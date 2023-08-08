from django.urls import path
from . import views


app_name = 'negotiation'
urlpatterns = [
    path('negotiate/<int:property_id>/', views.negotiation_form, name='negotiation_form'),  
    path('property/<int:property_id>/recent_negotiations',views.recent_negotiations, name = 'recent_negotiations') ,
    path('property/<int:property_id>/available_negotiations',views.available_negotiations, name = 'available_negotiations'),
    path('myoffers/',views.my_offers, name = 'my_offers'),
    path('my_negotiations/',views.my_negotiations, name = 'my_negotiations')
    
]
