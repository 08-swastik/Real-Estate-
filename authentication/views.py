# from django.shortcuts import render
# from django.contrib.auth.forms import UserCreationForm
# from .forms import SellerRegistrationForm

# def register(request):
#     form = SellerRegistrationForm()
#     if request.method == 'POST':
#         form = SellerRegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#         else:
#             form = SellerRegistrationForm()
#     return render(request, 'authentication/register.html', {'form': form})

# from django.shortcuts import render, redirect
# from .forms import CustomUserCreationForm
# from .models import Seller

# def register(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             # Create a new user
#             user = form.save()

#             # Create a corresponding seller entry
#             seller = Seller(user=user)
#             seller.save()

#             # Perform any additional actions or redirection
#             return redirect('home')
#     else:
#         form = CustomUserCreationForm()

#     # Render the registration form
#     context = {'form': form}
#     return render(request, 'authentication/register.html', context)

import datetime
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from .models import Seller

def register(request):
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

