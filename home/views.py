from django.shortcuts import render
from property_form.models import Property

# Create your views here.
def home(request):

    properties = Property.objects.all
    
    context = {
        'properties': properties
    }
    
    

    return render(request,'home/home.html',context)