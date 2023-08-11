from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('searchaddress/',views.address_search,name="search"),
    path('searchcity/',views.city_search,name="search"),

]