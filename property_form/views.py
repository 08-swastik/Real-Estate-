from django.shortcuts import render, redirect
from authentication.models import Seller
from django.contrib import messages
from .models import Property

def create_property(request):
        
        seller = Seller.objects.get(user=request.user)
    
        if request.method == 'POST':
            address = request.POST.get('address')
            square_feet = request.POST.get('square_feet')
            overview = request.POST.get('overview')
            bhk = request.POST.get('bhk')
            nearby_hospitals = request.POST.get('nearby_hospitals')
            nearby_schools = request.POST.get('nearby_schools')
            nearby_police_station = request.POST.get('nearby_police_station')
            price = request.POST.get('price')
            pictures = request.FILES.get('pictures')
            
            property_obj = Property.objects.create(
                seller=seller,
                address=address,
                square_feet=square_feet,
                overview=overview,
                bhk=bhk,
                nearby_hospitals=nearby_hospitals,
                nearby_schools=nearby_schools,
                nearby_police_station=nearby_police_station,
                price=price,
                pictures=pictures
            )

            property_obj.save() #for saving the property_obj to the database.
            
            return redirect('home')  # Redirect to the home page after successful submission
        
    
    
        context = {'seller': seller}
        return render(request, 'property_form/property_form.html', context)

def property_detail(request, property_id):
    property_instance = Property.objects.get(id=property_id)
    return render(request, 'property_form/property_detail.html', {'property': property_instance})



# Create your views here.
