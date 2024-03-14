from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm , UserCreationForm
from django.contrib.auth import login  , authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
user = get_user_model()
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.views import PasswordResetConfirmView
from .forms import *
from .models import *
from vendor.models import *
# Create your views here.
def index(request):
    return render(request , "customer/home.html")
def home_view(request):
    return render(request , "customer/home.html")
def about_us_view(request):
    return render(request , "customer/about_us.html")
def gallery_view(request):
    return render(request , "customer/gallery.html")
def service_view(request):
    services = Service.objects.all().order_by('-id')
    context ={
        'services':services
    }
    return render(request , "customer/service.html", context)
def contact_us_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            form = ContactForm()
    return render(request  , 'contact_us.html' , {'form':form})

# Detial View of profile
def user_profile_detail_view(request):
    user_profile = User_Profile.objects.get(user=request.user)
    
    return render(request, 'customer/profile.html', {'user_profile': user_profile})


# Edit Detail view of Profile
def user_profile_edit_view(request):
    user_profile = User_Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES ,  instance=user_profile)
        if form.is_valid():
            user = form.save(commit=False)
            user_profile.user = request.user  # Ensure the user is set correctly
            user.save()
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.mobile_no = form.cleaned_data['mobile_no']
            user.save()
            messages.success(request, 'Profile successfully updated.')
            return redirect('customer:user_profile_detail_view')
        else:
            print("Form is not valid:", form.errors)
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'customer/profile.html', {'form': form})