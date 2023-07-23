from django.urls import path
from . import views


app_name = 'negotiation'
urlpatterns = [
    path('negotiate/', views.negotiation_form, name='negotiation_form'),   
]