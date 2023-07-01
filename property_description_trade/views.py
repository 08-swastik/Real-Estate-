from django.shortcuts import get_object_or_404, redirect, render
from property_form.models import Property
from django.contrib.auth.decorators import login_required


# Create your views here.
def property_detail(request,property_id):

    property_obj = get_object_or_404(Property, id=property_id)
    
    
    context = {
        'property_image': property_obj.pictures.url,
        'property_address': property_obj.address,
        'property_price': property_obj.price,
        'bhk': property_obj.bhk,
        'property_sqft': property_obj.square_feet,
        'property_overview': property_obj.overview,
        'nearby_schools' : property_obj.nearby_schools,
        'nearby_PS' : property_obj.nearby_police_station,
        'nearby_hospital' : property_obj.nearby_hospitals,
        'isAuthenticated': request.user.is_authenticated,
    }

    return render(request,'property_description_trade/property_description.html', context)

@login_required(login_url='authentication:signin')
def payment(request,property_id) :

    property = get_object_or_404(Property, id=property_id)

    if request.method == 'POST':
        billing_name = request.POST.get('billing_name')
        # Do something with the billing name
        
        # Redirect to the confirmation page
        return redirect('property_description_trade:confirmation',property_id=property_id,billing_name=billing_name)

    context = {
        'property': property,
        'property_price': property.price,
    }


    return render(request,'property_description_trade/payment.html',context)

# @login_required(login_url='authentication:signin')
def confirmation(request,property_id,billing_name) :

    property = get_object_or_404(Property, id=property_id)

    context = {
        'property': property,
        'property_price': property.price,
        'billing_name': billing_name,
    }


    return render(request,'property_description_trade/confirmation.html',context)
