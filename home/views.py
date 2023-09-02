from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import render
from property_form.models import Property
from negotiation.models import Negotiation
import schedule
from negotiation.negotiation_utils import expiry_check

# Create your views here.
def home(request):


    if hasattr(request, 'user') and request.user.is_authenticated:

        expiry_check(request.user)

    properties = Property.objects.all

    context = {
        'properties': properties,
    }


    return render(request,'home/home.html',context)



def address_search(request):
    
    address_query = request.GET.get('address', '')
    search_results = Property.objects.filter(address__icontains=address_query)
    
    
    data = [{'address': property.address} for property in search_results]
    
    return JsonResponse(data, safe=False)    

def city_search(request):

    city_query = request.GET.get('city', '')
    search_results = Property.objects.filter(city__icontains=city_query)
    

    data = [{'city': property.city} for property in search_results]

    return JsonResponse(data, safe=False)

