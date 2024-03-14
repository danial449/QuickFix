from django import forms 
from .models import *
from django.contrib.auth.forms import UserCreationForm


class VendorProfileForm(forms.ModelForm):

    class Meta:
        model = Vendor_Profile
        fields = "__all__"

class ServiceCreateForm(forms.ModelForm):
    
    class Meta:
        model = Service
        fields = "__all__"

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['user', 'service']