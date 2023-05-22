from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    address = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'address', 'phone_number','password1','password2']

class SellerLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class ClientCreationForm(UserCreationForm):
    address = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'address', 'phone_number','password1','password2']

class ClientLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password'] 