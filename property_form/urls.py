from django.urls import path
from . import views

app_name = 'property_form'

urlpatterns = [
    path('add_listing', views.create_property, name='create_property'),
    path('detail/<int:property_id>/', views.property_detail, name='property_detail'),
    # Add other URLs for property listing modification, deletion, etc.
]
