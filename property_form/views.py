from django.shortcuts import render,get_object_or_404, redirect
from authentication.models import Seller
from .models import Property

def create_property(request):
        
    seller = Seller.objects.get(user=request.user)

    if request.method == 'POST':
        address = request.POST.get('address')
        city = request.POST.get('address')
        square_feet = request.POST.get('square_feet')
        overview = request.POST.get('overview')
        bhk = request.POST.get('bhk')
        price = request.POST.get('price')
        pictures = request.FILES.get('pictures')
        
        property_obj = Property.objects.create(
            seller=seller,
            address=address,
            city = city,
            square_feet=square_feet,
            overview=overview,
            bhk=bhk,
            price=price,
            pictures=pictures
        )

        property_obj.save() 
        
        return redirect('home')  



    context = {'seller': seller}
    return render(request, 'property_form/property_form.html', context)

def my_listings(request) :
    user = request.user
    
    
    if hasattr(user,'seller'):
          seller = user.seller
          properties = Property.objects.filter(seller=seller)
          


    context = {
        'properties': properties,
        
        
    }
    return render(request, 'property_form/my_listings.html', context)
     

def properties(request):
    city = request.GET.get('city')
    address = request.GET.get('address')

    # Filter properties based on provided city and address
    if city and address:
        properties = Property.objects.filter(city__icontains=city, address__icontains=address)
    elif city:
        properties = Property.objects.filter(city__icontains=city)
    elif address:
        properties = Property.objects.filter(address__icontains=address)
    else:
        properties = []

    context = {
        'properties': properties,
        'searched_city': city,
        'searched_address': address,
    }

    return render(request, 'property_form/properties.html', context)

# Create your views here.

def update_property(request, property_id):
     
    property_obj = Property.objects.get(id=property_id)

    if request.method == 'POST':
        property_obj.address = request.POST.get('address')
        property_obj.city = request.POST.get('city')
        property_obj.square_feet = request.POST.get('square_feet')
        property_obj.overview = request.POST.get('overview')
        property_obj.bhk = request.POST.get('bhk')
        property_obj.price = request.POST.get('price')
        
        pictures = request.FILES.get('pictures')
        if pictures:
            property_obj.pictures = pictures
        
        property_obj.save()  
        
        return redirect('property_form:my_listings')  
    
    context = {'property': property_obj}
    return render(request, 'property_form/property_update.html', context)


def delete_property(request,property_id):
     
     property_obj = get_object_or_404(Property, id = property_id)

     if request.method == "POST":
          
          property_obj.delete()
          return redirect('property_form:my_listings')  
     
    #  context = {'property' : property_obj}

    #  return render(request,'property_form/delete_property.html', context)