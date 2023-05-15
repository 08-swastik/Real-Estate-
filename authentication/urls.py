from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('seller_register',views.seller_register,name="register"),
    path('seller_login',views.seller_login,name="login"),

]