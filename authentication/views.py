from django.contrib import messages
import datetime
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm , SellerLoginForm,ClientCreationForm,ClientLoginForm
from .models import Seller,Client
from django.contrib.auth import authenticate, login

#seller registration
def seller_register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Create a new user
            user = form.save()

            # Create a corresponding seller entry
            seller = Seller(user = user,username = form.cleaned_data.get('username'),first_name=form.cleaned_data.get('first_name'), last_name=form.cleaned_data.get('last_name'),email=form.cleaned_data.get('email'),address=form.cleaned_data.get('address'),registration_date = datetime.datetime.now(),phone_number = form.cleaned_data.get('phone_number') )
            
            seller.save()

            # Perform any additional actions or redirection
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('authentication:login')
    else:
        form = CustomUserCreationForm()

    # Render the registration form
    context = {'form': form}
    return render(request, 'authentication/register.html', context)

#seller login
def seller_login(request):
    if request.method == 'POST':
        form = SellerLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                # User is not registered
                messages.error(request, "User is not registered. Please register as a Seller.")
                form = SellerLoginForm()
        else:
            # Invalid login credentials
            messages.error(request, "Invalid login credentials.")
    else:
        form = SellerLoginForm()

    context = {'form': form}
    return render(request, 'authentication/seller_login.html', context)

#client register
def client_register(request):
    if request.method == 'POST':
        form = ClientCreationForm(request.POST)
        if form.is_valid():
            # Create a new user
            user = form.save()

            # Create a corresponding seller entry
            client = Client(user = user,username = form.cleaned_data.get('username'),first_name=form.cleaned_data.get('first_name'), last_name=form.cleaned_data.get('last_name'),email=form.cleaned_data.get('email'),address=form.cleaned_data.get('address'),registration_date = datetime.datetime.now(),phone_number = form.cleaned_data.get('phone_number') )
            
            client.save()

            # Perform any additional actions or redirection
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('authentication:client_login')
    else:
        form = ClientCreationForm()

    # Render the registration form
    context = {'form': form}
    return render(request, 'authentication/register_client.html', context)

#client login
def client_login(request):
    if request.method == 'POST':
        form = ClientLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                # User is not registered
                messages.error(request, "User is not registered. Please register as a Seller.")
                form = ClientLoginForm()
        else:
            # Invalid login credentials
            messages.error(request, "Invalid login credentials.")
    else:
        form = ClientLoginForm()

    context = {'form': form}
    return render(request, 'authentication/client_login.html', context)
