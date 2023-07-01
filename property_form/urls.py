from django.urls import path
from . import views

app_name = 'property_form'

urlpatterns = [
    path('add_listing', views.create_property, name='create_property'),
    
    path('properties',views.properties,name="properties"),
]


