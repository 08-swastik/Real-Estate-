from django import forms
from .models import Property

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['address', 'square_feet', 'overview', 'nearby_schools', 'nearby_police_stations', 'price', 'pictures']
        # widgets = {
        #     'nearby_schools': forms.CheckboxSelectMultiple(),
        #     'nearby_police_stations': forms.CheckboxSelectMultiple(),
        # }
