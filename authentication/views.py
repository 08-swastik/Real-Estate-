import datetime
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm , SellerLoginForm
from .models import Seller
from django.contrib.auth import authenticate, login

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
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    # Render the registration form
    context = {'form': form}
    return render(request, 'authentication/register.html', context)

def seller_login(request):
    if request.method == 'POST':
        form = SellerLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_seller:
                login(request, user)
                # Redirect to the seller's dashboard or home page
                # return redirect('seller_dashboard')
            else:
                # Invalid login credentials or the user is not a seller
                form.add_error(None, "Invalid login credentials")
    else:
        form = SellerLoginForm()

    context = {'form': form}
    return render(request, 'authentication/seller_login.html', context)