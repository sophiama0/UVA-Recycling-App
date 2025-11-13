from django import forms
from django.contrib.auth.models import User

from .models import UserProfile, RecyclingBin


class RecyclingBinForm(forms.ModelForm):
    class Meta:
        model = RecyclingBin
        fields = ['name', 'description', 'latitude', 'longitude', 'fullness', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'fullness': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 1, 'step': 0.01}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class RecyclingBinUpdateForm(forms.ModelForm):
    class Meta:
        model = RecyclingBin
        fields = ['name', 'description', 'latitude', 'longitude', 'fullness', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'fullness': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 1, 'step': 0.01}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user and self.instance.posted_by != user:
            for field in ['name', 'description', 'latitude', 'longitude', 'image']:
                self.fields[field].disabled = True


class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class UserNameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'})
        }


class RecyclingFullnessForm(forms.Form):
    """Accepts fullness as a percentage (0-100)."""
    fullness_percent = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
    )