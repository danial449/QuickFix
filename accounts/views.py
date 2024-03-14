from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth import login  , authenticate, logout
from django.urls import reverse
from django.contrib import messages
from .forms import LoginForm , CustomerSignUpForm , VendorSignUpForm
from customer.models import User_Profile
from vendor.models import Vendor_Profile
# Create your views here.

def user_register_view(request):
    msg = None
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save to the database yet
            user.is_customer = True  # Set any additional attributes if needed
            user.is_staff = False  
            user.save()  # Save the user using the manager of your custom User model
            msg = 'User Created'
            # making profile during registration
            profile = User_Profile.objects.create(
                user=user,
                first_name=user.first_name,
                last_name=user.last_name,
                username=user.username,
                email=user.email,
                mobile_no=user.mobile_no,
                user_image=user.user_image
            )
            return redirect('accounts:user_login_view')
        else:
            print("Form is not valid:", form.errors)
    else:
        form = CustomerSignUpForm()
    return render(request , "accounts/register.html", {'form':form , 'msg':msg})

def vendor_register_view(request):
    msg = None
    if request.method == 'POST':
        form = VendorSignUpForm(request.POST , request.FILES)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save to the database yet
            user.is_vendor = True  # Set any additional attributes if needed
            user.is_staff = False  
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
                vendor_image =user.vendor_image,    
            )
            return redirect('accounts:user_login_view')
        else:
            print("Form is not valid:", form.errors)
    else:
        form = VendorSignUpForm()
    return render(request , "accounts/vendor_register.html", {'form':form , 'msg':msg})


# def admin_register_view(request):
#     msg = None
#     if request.method == 'POST':
#         form = AdminSignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)  # Don't save to the database yet
#             user.is_admin = True  # Set any additional attributes if needed
#             user.is_staff = True  
#             user.save()  # Save the user using the manager of your custom User model
#             msg = 'Admin Created'
#             return redirect('accounts:user_login_view')
#         else:
#             print("Form is not valid:", form.errors)
#     else:
#         form = AdminSignUpForm()
#     return render(request , "accounts/admin_register.html", {'form':form , 'msg':msg})


def user_login_view(request):
    msg = None
    if request.method == 'POST':
        form = LoginForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # Authenticate user
            user = authenticate(username=username, password=password)
            
            if user is not None and user.is_customer:
                login(request, user)
                return redirect('customer:home')
            elif user is not None and user.is_vendor:
                login(request, user)
                return redirect('customer:home')
            elif user is not None and user.is_admin:
                login(request, user)
                return redirect('customer:home')
            else:
                msg = 'Invalid Credentials'
            
        else:   
            print(form.errors)
    else:
        form = LoginForm()
    return render(request , 'accounts/login.html', {'form':form , 'msg':msg})

def user_logout_view(request):
    logout(request)
    return redirect('customer:home')
