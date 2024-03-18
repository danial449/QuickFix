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
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
# Create your views here.
def home_view(request):
    services = Service.objects.all().order_by('-id')[:6]
    return render(request , "customer/home.html", {'services':services})

def about_us_view(request):
    return render(request , "customer/about_us.html")

def service_view(request):
    services = Service.objects.all().order_by('-id')
    categories = Service_Category.objects.all()
    # pagination of services
    paginator = Paginator(services , 6)
    page_number = request.GET.get('page')
    servicefinal = paginator.get_page(page_number)
    totalpage = servicefinal.paginator.num_pages

    context ={
        'services':servicefinal,
        'categories':categories,
        'totalpagelist' : [n+1 for n in range(totalpage)]
    }
    return render(request , "customer/service.html", context)

def contact_us_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been successfully submitted! We'll get back to you as soon as possible. Thank you for reaching out.")
            return redirect('customer:contact')
        else:
            print(form.errors)
    else:
        form = ContactForm()
    return render(request  , 'customer/contact_us.html' , {'form':form})

@login_required
# Detial View of profile
def user_profile_detail_view(request):
    user_profile = User_Profile.objects.get(user=request.user)
    
    return render(request, 'customer/profile.html', {'user_profile': user_profile})

@login_required
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