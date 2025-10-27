from django import forms
from .models import RecyclingSpot # Import your model

class RecyclingSpotForm(forms.ModelForm):
    class Meta:
        model = RecyclingSpot
        
        fields = ['title', 'address', 'description']
       