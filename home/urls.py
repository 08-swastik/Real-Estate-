from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('search/',views.property_search,name="search"),
]