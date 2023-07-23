# views.py

from django.shortcuts import render, redirect
from .models import Negotiation


def negotiation_form(request):
    user = request.user

        
    if hasattr(user, 'seller'):
        seller_or_client = user.seller
    elif hasattr(user, 'client'):
        seller_or_client = user.client

    print(seller_or_client)    

    if request.method == 'POST':
        requested_price = request.POST['requested-price']
        
        
        
        email = seller_or_client.email
        first_name = seller_or_client.first_name
        last_name = seller_or_client.last_name
        phone_number = seller_or_client.phone_number

        
        negotiation = Negotiation.objects.create(
            user=user,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,  
            requested_price=requested_price,
        )

        negotiation.save()

        
        return redirect('property_description')

    # Handle GET request if needed
    return render(request, 'property_description_trade/property_description.html',{'seller_or_client': seller_or_client})


# Create your views here.
