from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# class SellerRegistrationForm(UserCreationForm):
    
#     phone_number = forms.IntegerField()
#     address = forms.CharField(max_length=100)

#     class Meta:
#         model = User
#         fields = ['username','first_name', 'last_name', 'email', 'phone_number', 'address', 'password1', 'password2']

from django import forms
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    address = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'address', 'phone_number']

class SellerLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']