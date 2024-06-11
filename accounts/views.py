from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth import login  , authenticate, logout
from django.urls import reverse
from django.contrib import messages
from .forms import LoginForm , CustomerSignUpForm , VendorSignUpForm
from customer.models import User_Profile
from vendor.models import Vendor_Profile
from .models import User
import uuid
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

def user_register_view(request):

    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save to the database yet
            user.is_customer = True  # Set any additional attributes if needed
            user.is_staff = False  
            user.is_email_verified = False
            user.email_verification_token = str(uuid.uuid4())
            user.save()  # Save the user using the manager of your custom User model

            # making profile during registration
            profile = User_Profile.objects.create(
                user=user,
                first_name=user.first_name,
                last_name=user.last_name,
                username=user.username,
                email=user.email,
                mobile_no=user.mobile_no,
                user_image=request.FILES.get('vendor_image')
            )

            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            activation_link = f'http://{current_site}/accounts/verify_email/{user.email_verification_token}/'
            message = f'click the link to activate your account:{activation_link}'
            email_from = settings.DEFAULT_FROM_EMAIL
            recipeient_list = [user.email]
            send_mail(subject, message, email_from, recipeient_list)

            messages.success(request, "Thank you for registering! Please check your email to verify your account before logging in.")

            return redirect('accounts:user_login_view')
        else:
            print("Form is not valid:", form.errors)
    else:
        form = CustomerSignUpForm()
    return render(request , "accounts/register.html", {'form':form})

def vendor_register_view(request):
    
    if request.method == 'POST':
        form = VendorSignUpForm(request.POST , request.FILES)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save to the database yet
            user.is_vendor = True  # Set any additional attributes if needed
            user.is_staff = False  
            user.is_email_verified = False
            user.email_verification_token = str(uuid.uuid4())
            user.save()  # Save the user using the manager of your custom User model
            msg = 'User Created'
            profile = Vendor_Profile.objects.create(
                user=user,
                first_name=user.first_name,
                last_name=user.last_name,
                username=user.username,
                email=user.email,
                address1 =user.address1,
                mobile_no =user.mobile_no,
                address2 =user.address2,
                city =user.city,
                province =user.province,
                employee =user.employee,
                cnic =user.cnic,
                shop_reference =user.shop_reference,
                vendor_image =request.FILES.get('vendor_image')   
            )

            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            activation_link = f'http://{current_site}/accounts/verify_email/{user.email_verification_token}/'
            message = f'click the link to activate your account:{activation_link}'
            email_from = settings.DEFAULT_FROM_EMAIL
            recipeient_list = [user.email]
            send_mail(subject, message, email_from, recipeient_list)

            messages.success(request, "Thank you for registering! Please check your email to verify your account before logging in.")

            return redirect('accounts:user_login_view')
        else:
            print("Form is not valid:", form.errors)
    else:
        form = VendorSignUpForm()
    return render(request , "accounts/vendor_register.html", {'form':form})

def verify_email_view(request , token):
    try:
        user = User.objects.get(email_verification_token = token)
        if user:
           user.is_email_verified = True
           user.email_verification_token = None
           user.save()
           return redirect('accounts:user_login_view')
    except:
        return HttpResponse("Activation Link is Invalid")

def user_login_view(request):
    msg = None
    if request.method == 'POST':
        form = LoginForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # Authenticate user
            user = authenticate(username=username, password=password)
            
            if user is not None and user.is_customer and user.is_email_verified:
                login(request, user)
                return redirect('customer:home')
            elif user is not None and user.is_vendor and user.is_email_verified:
                login(request, user)
                return redirect('customer:home')
            else:
                messages.success(request, 'Invalid Credentials')
            
        else:   
            print(form.errors)
    else:
        form = LoginForm()
    return render(request , 'accounts/login.html', {'form':form})

def user_logout_view(request):
    logout(request)
    return redirect('customer:home')
