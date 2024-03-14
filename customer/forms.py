from django import forms 
from .models import *

class ContactForm(forms.ModelForm):
    
    class Meta:
        model = ContactUs
        fields = "__all__"

        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User_Profile
        fields = "__all__"