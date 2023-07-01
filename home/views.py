from django.http import JsonResponse
from django.shortcuts import render
from property_form.models import Property

# Create your views here.
def home(request):

    properties = Property.objects.all

    context = {
        'properties': properties,
    }
    
    

    return render(request,'home/home.html',context)


def property_search(request):
    search_query = request.GET.get('query', '')
    search_results = Property.objects.filter(address__icontains=search_query)
    
    # Process search results and return the data as JSON
    data = [{'address': property.address} for property in search_results]
    
    return JsonResponse(data, safe=False)    