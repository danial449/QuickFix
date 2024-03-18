from django import forms 
from .models import *
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs = {"class":"form-control"}))
    password = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs = {"class":"form-control"}))

class CommonSignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs = {"class":"form-control"}))
    password1 = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs = {"class":"form-control"}))
    password2 = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs = {"class":"form-control"}))
    email = forms.CharField(max_length=30, required=True, widget=forms.EmailInput(attrs = {"class":"form-control"}))
    
    class Meta:
        model = User
        fields = ('first_name' , 'last_name', 'username' , 'email' , 'password1' , 'password2')

class CustomerSignUpForm(CommonSignUpForm):
    class Meta:
        model = User
        fields = CommonSignUpForm.Meta.fields + ('mobile_no',)


class VendorSignUpForm(CommonSignUpForm):
    CATAGORY_CHOICES = [
        ('Punjab', 'Punjab'),
        ('Sindh', 'Sindh'),
        ('Khyber Pakhtunkhwa', 'Khyber Pakhtunkhwa'),
        ('Gilgit-Baltistan', 'Gilgit-Baltistan'),
        ('Islamabad Capital Territory', 'Islamabad Capital Territory'),
        ('Balochistan', 'Balochistan'),
    ]

    CATAGORY_EMP = [
        ('Electrician', 'Electrician'),
        ('Plumber', 'Plumber'),
        ('Sweaper', 'Sweaper'),
        ('Carpenter', 'Carpenter'),
        ('Drain clean', 'Drain clean'),
        ('AC repair', 'AC repair'),
        ('Painting & Decorating', 'Painting & Decorating'),
    ]

    mobile_no = forms.CharField(max_length=11, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    address1 = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    address2 = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    city = forms.CharField(max_length=70, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    province = forms.ChoiceField(choices=CATAGORY_CHOICES, required=False, widget=forms.Select(attrs={"class": "form-control"}))
    employee = forms.ChoiceField(choices=CATAGORY_EMP, required=False, widget=forms.Select(attrs={"class": "form-control"}))
    cnic = forms.CharField(max_length=13, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    shop_reference = forms.CharField(max_length=200, required=False, widget=forms.Textarea(attrs={"class": "form-control"}))
    vendor_image = forms.ImageField(required=False)

    class Meta(CommonSignUpForm.Meta):
        model = User
        fields = CommonSignUpForm.Meta.fields + ('mobile_no', 'address1', 'address2', 'city', 'province', 'employee', 'cnic', 'shop_reference', 'vendor_image' , 'is_email_verified' , 'email_verification_token')


