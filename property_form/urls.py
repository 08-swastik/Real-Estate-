from django.urls import path
from . import views

app_name = 'property_form'

urlpatterns = [
    path('add_listing', views.create_property, name='create_property'),
    path('my-listings', views.my_listings, name='my_listings'),
    path('properties',views.properties,name="properties"),
    path('update/<int:property_id>/', views.update_property, name='update_property'),
    path('property/<int:property_id>/delete/',views.delete_property, name= 'delete_property'),
    
]


