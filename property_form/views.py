from django.shortcuts import render, redirect
from .forms import PropertyForm
from .models import Property

def create_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_instance = form.save(commit=False)
            property_instance.seller = request.user
            property_instance.save()
            form.save_m2m()  # Save many-to-many relationships
            return redirect('property_detail', property_id=property_instance.id)
    else:
        form = PropertyForm()
    
    return render(request, 'property_form/property_form.html', {'form': form})

def property_detail(request, property_id):
    property_instance = Property.objects.get(id=property_id)
    return render(request, 'property_form/property_detail.html', {'property': property_instance})

# Other views for property listing modification, deletion, etc.

# Create your views here.
