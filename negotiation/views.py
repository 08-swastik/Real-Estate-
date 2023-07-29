# views.py

from django.db.models import Q
from django.shortcuts import render, redirect,get_object_or_404
from .models import Negotiation
from property_form.models import Property


def negotiation_form(request,property_id):



    if request.method == 'POST':
        user = request.user
        requested_price = request.POST.get('requested_price')

            
        if hasattr(user, 'seller'):
            seller_or_client = user.seller
        elif hasattr(user, 'client'):
            seller_or_client = user.client
        
    
        email = seller_or_client.email
        first_name = seller_or_client.first_name
        last_name = seller_or_client.last_name
        phone_number = seller_or_client.phone_number

        property_obj = get_object_or_404(Property, id=property_id)
        
        negotiation = Negotiation.objects.create(
            user=user,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,  
            requested_price=requested_price,
            property=property_obj,
        )

        negotiation.save()
        return redirect('home')
            


def recent_negotiations(request,property_id):

    if property_id:
        negotiations = Negotiation.objects.filter(property_id=property_id).order_by('-requested_price')
    else:
        negotiations = Negotiation.objects.none()

    if property_id is not None:
        property_obj = Property.objects.get(id=property_id)
        original_price = property_obj.price
    else:
        property_obj = None
        original_price = None

    return render(request, 'negotiations/recent_negotiations.html', {
        'negotiations': negotiations,
        'original_price': original_price,
    })    



def available_negotiations(request, property_id):
    if request.method == 'POST':
        negotiations = Negotiation.objects.filter(property_id=property_id).order_by('-requested_price')
        original_price = None

        for negotiation in negotiations:
            status = request.POST.get(str(negotiation.id))  
            if status in ['pending', 'rejected', 'accepted']:
                negotiation.status = status
                negotiation.save()

        return redirect('home')       
            

        
    else:
        if property_id:
            negotiations = Negotiation.objects.filter(property_id=property_id).order_by('-requested_price')
            property_obj = Property.objects.get(id=property_id)
            original_price = property_obj.price
        

    return render(request, 'negotiations/available_negotiations.html', {
        'negotiations': negotiations,
        'original_price': original_price,
        'property_obj': property_obj,
    }) 


def my_offers(request):
    accepted_negotiations = Negotiation.objects.filter(user=request.user, status = 'accepted', property__status='available')
    return render(request,'negotiations/my_offers.html',{'accepted_negotiations': accepted_negotiations})   


def my_negotiations(request):
    negotiations = Negotiation.objects.filter(user=request.user, status = 'accepted', property__status='available')
    return render(request,'negotiations/my_negotiations.html',{'negotiations': negotiations})

