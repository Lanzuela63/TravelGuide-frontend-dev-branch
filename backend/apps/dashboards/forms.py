# backend/apps/dashboards/forms.py
from django import forms
from apps.tourism.models import TouristSpot, CityMunicipality
from apps.users.models import CustomUser
from apps.ar.models import ARScene
from apps.business.models import Business, BusinessCategory
from apps.events.models import Event

class TouristSpotForm(forms.ModelForm):
    class Meta:
        model = TouristSpot
        fields = [
            'name',
            'description',
            'city',
            'image',
            'is_featured',
            'is_active',
            'show_in_carousel',
            'entrance_fee',
            'operating_hours',
            'contact_number',
            'email',
            'website',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'city': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'show_in_carousel': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'entrance_fee': forms.NumberInput(attrs={'class': 'form-control'}),
            'operating_hours': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
        }

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'role',
            'is_active',
            'is_staff',
            'bio',
            'profile_image',
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class ARSceneForm(forms.ModelForm):
    class Meta:
        model = ARScene
        fields = [
            'name',
            'description',
            'model_file',
            'marker_image',
            'latitude',
            'longitude',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'model_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'marker_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = [
            'owner',
            'name',
            'description',
            'address',
            'city',
            'latitude',
            'longitude',
            'phone_number',
            'email',
            'website',
            'category',
            'logo',
            'cover_image',
            'opening_hours',
            'is_approved',
            'is_active',
        ]
        widgets = {
            'owner': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-select'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'cover_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'opening_hours': forms.TextInput(attrs={'class': 'form-control'}),
            'is_approved': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'organizer',
            'title',
            'description',
            'location',
            'date',
            'time',
            'is_approved',
            'status',
        ]
        widgets = {
            'organizer': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'is_approved': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }