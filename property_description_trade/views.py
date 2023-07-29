from django.shortcuts import get_object_or_404, redirect, render
from property_form.models import Property
from django.contrib.auth.decorators import login_required
from negotiation.models import Negotiation


# Create your views here.
def property_detail(request,property_id):

    property_obj = get_object_or_404(Property, id=property_id)
    user = request.user

    accepted_negotiation = Negotiation.objects.filter(user = request.user,property=property_obj, status='accepted').first()
    actual_price = property_obj.price
    property_price = None
    
    if accepted_negotiation:
        property_price = accepted_negotiation.requested_price

        
        
    
        
    if hasattr(user, 'seller'):
        seller_or_client = user.seller
    elif hasattr(user, 'client'):
        seller_or_client = user.client
    
    
    is_sold = property_obj.status == 'sold'

    context = {
        'property_image': property_obj.pictures.url,
        'property_address': property_obj.address,
        'property_price': actual_price,
        'special_price' : property_price,
        'bhk': property_obj.bhk,
        'property_sqft': property_obj.square_feet,
        'property_overview': property_obj.overview,
        'nearby_schools' : property_obj.nearby_schools,
        'nearby_PS' : property_obj.nearby_police_station,
        'nearby_hospital' : property_obj.nearby_hospitals,
        'isAuthenticated': request.user.is_authenticated,
        'seller_or_client' : seller_or_client,
        'property_id': property_id,
        'property_obj' : property_obj,
        'is_sold': is_sold,

    }

    return render(request,'property_description_trade/property_description.html', context)

@login_required(login_url='authentication:signin')
def payment(request,property_id) :

    property = get_object_or_404(Property, id=property_id)

    if request.method == 'POST':
        billing_name = request.POST.get('billing_name')
        
        return redirect('property_description_trade:confirmation',property_id=property_id,billing_name=billing_name)
    
    negotiation = Negotiation.objects.filter(user = request.user ,property=property, status='accepted').first()

    
    property_price = negotiation.requested_price if negotiation  else property.price

    context = {
        'property': property,
        'property_price': property_price,
    }


    return render(request,'property_description_trade/payment.html',context)

# @login_required(login_url='authentication:signin')
def confirmation(request,property_id,billing_name) :

    property = get_object_or_404(Property, id=property_id)

    negotiation = Negotiation.objects.filter(user = request.user ,property=property, status='accepted').first()

    
    property_price = negotiation.requested_price if negotiation  else property.price

    property.status = 'sold'
    property.save()

    context = {
        'property': property,
        'property_price': property_price,
        'billing_name': billing_name,

    }


    return render(request,'property_description_trade/confirmation.html',context)
