from django.shortcuts import render , redirect ,get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from .forms import *
from .models import *
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def vendor_profile_detail_view(request):
    vendor_profile = Vendor_Profile.objects.get(user=request.user)
    
    return render(request, 'vendor/profile.html', {'vendor_profile': vendor_profile})



@login_required
def vendor_profile_edit_view(request):
    vendor_profile = Vendor_Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = VendorProfileForm(request.POST, request.FILES ,  instance=vendor_profile)
        if form.is_valid():
            user = form.save(commit=False)
            vendor_profile.user = request.user  # Ensure the user is set correctly
            user.save()
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.mobile_no = form.cleaned_data['mobile_no']
            user.address1 = form.cleaned_data['address1']
            user.address2 = form.cleaned_data['address2']
            user.city = form.cleaned_data['city']
            user.province = form.cleaned_data['province']
            user.employee = form.cleaned_data['employee']
            user.cnic = form.cleaned_data['cnic']
            user.shop_reference = form.cleaned_data['shop_reference']
            user.vendor_image = form.cleaned_data['vendor_image']
            user.save()
            messages.success(request, 'Profile successfully updated.')
            return redirect('vendor:vendor_profile_detail_view')
        else:
            print("Form is not valid:", form.errors)
    else:
        form = VendorProfileForm(instance=vendor_profile)

    return render(request, 'vendor/profile.html', {'form': form})

@login_required
def service_add_view(request):
    categories = Service_Category.objects.all()
    if request.method == 'POST':
        form = ServiceCreateForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.user = request.user  # Assign the current user to the service's user field
            service.save()
            return redirect('vendor:my_service_detail_view' , id=request.user.id)
        else:
            print(form.errors)
    else:
        form = ServiceCreateForm()
    return render(request, 'vendor/Service_create_form.html', {'form': form , 'categories': categories})

@login_required
def my_service_detail_view(request, id):
    user = User.objects.get(id=id)  # Replace Vendor with your actual vendor model

    # Filter services based on the current vendor
    services = Service.objects.filter(user=request.user)

    return render(request, 'vendor/my_services.html', {'services': services, 'user': user})

def service_detail_view(request, service_id):
    service = Service.objects.get(id=service_id)
    feedback = service.feedback.all()
    # pagination of feedback
    paginator = Paginator(feedback , 5)
    page_number = request.GET.get('page')
    feedbackfinal = paginator.get_page(page_number)
    totalpage = feedbackfinal.paginator.num_pages

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feeback=form.save(commit=False)
            feeback.service = service
            feeback.user = request.user
            feeback.save()
            messages.success(request, "Submit Successfully! Thank you for your feedback.")
            return redirect('vendor:service_detail_view' , service_id=service.id)
        else:
            print(form.errors)
    else:
        form=FeedbackForm()
    
    context = {
        'service': service ,
        'feedback':feedbackfinal,
        'totalpagelist' : [n+1 for n in range(totalpage)]
    }
    return render(request, 'vendor/service_detail.html', context)

def service_in_category(request , category_id):
    categories = Service_Category.objects.all()
    category = Service_Category.objects.get(id=category_id)
    services = category.services.all()
    # pagination of services
    paginator = Paginator(services , 6)
    page_number = request.GET.get('page')
    servicefinal = paginator.get_page(page_number)
    totalpage = servicefinal.paginator.num_pages

    context = {
        'categories':categories,
        'category':category,
        'services':servicefinal,
        'totalpagelist' : [n+1 for n in range(totalpage)]
    }
    return render(request , "vendor/service_in_category.html" , context)

@login_required
def delete_service_view(request , service_id):
    service = Service.objects.get(id=service_id)
    service.delete()
    messages.success(request, "Service successfully deleted. If you need further assistance, feel free to contact us.")
    return redirect('vendor:my_service_detail_view' , id=request.user.id)

@login_required
def book_service_view(request, service_id):
    service = Service.objects.get(id=service_id)

    if request.method == 'POST':
        # Get user details
        user = request.user
        mobile_no = user.mobile_no
        email = user.email
        status = 'Pending'

        # Create and save booking
        booking = Booking(
            service=service,
            user=user,
            mobile_no=mobile_no,
            email=email,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            status=status
        )
        booking.save()
        messages.success(request, "Service Booked Successfully")
        return redirect('vendor:user_dashboard')

    return render(request, 'vendor/user_dashboard.html', {'service': service})

@login_required
def delete_booking_view(request , booking_id):
    booking = Booking.objects.get(id=booking_id)
    booking.delete()
    messages.success(request, "Booking successfully deleted. If you need further assistance, feel free to contact us.")
    return redirect('vendor:vendor_dashboard')

@login_required
def vendor_dashboard_view(request):
    # Get services created by the vendor
    vendor_services = Service.objects.filter(user=request.user)

    # Get bookings associated with the vendor's services
    bookings = Booking.objects.filter(service__in=vendor_services).order_by('-id')

    # pagination of services
    paginator = Paginator(bookings , 10)
    page_number = request.GET.get('page')
    bookingfinal = paginator.get_page(page_number)
    totalpage = bookingfinal.paginator.num_pages

    context = {
        'bookings': bookingfinal,
        'totalpagelist' : [n+1 for n in range(totalpage)]
    }

    return render(request, 'vendor/vendor_dashboard.html', context)

@login_required
def user_dashboard_view(request):
    # Retrieve bookings for the current user
    bookings = Booking.objects.filter(user=request.user).order_by('-id')

    # Create a list to store details of each booking along with the service creator's details
    booking_details = []

    for booking in bookings:
        # Fetch service creator details for each booking
        service_creator = User.objects.get(id=booking.service.user_id)

        # Append booking details along with service creator's details to the list
        booking_detail = {
            'booking': booking,
            'service_creator': service_creator
        }
        booking_details.append(booking_detail)

        # pagination of services
        paginator = Paginator(booking_details , 10)
        page_number = request.GET.get('page')
        bookingfinal = paginator.get_page(page_number)
        totalpage = bookingfinal.paginator.num_pages
    
        context = {
            'booking_details': bookingfinal,
            'totalpagelist' : [n+1 for n in range(totalpage)]
        }

    # Pass booking details to the template
    return render(request, 'vendor/user_dashboard.html', context)

@login_required
def approve_booking_view(request, booking_id, status):
    booking = get_object_or_404(Booking, id=booking_id)

    # Additional logic to set the approved time and update other details
    if status == 'Booked':
        booking.status = 'Booked'
        messages.success(request, "Booking successfully approved. Thank you for confirming!")
       
        # Additional logic for booked status if needed
    elif status == 'Cancelled':
        booking.status = 'Cancelled'
        messages.success(request, "Booking successfully cancelled. We hope to assist you with future bookings.")
        # Additional logic for cancelled status if needed

    booking.save()

    return redirect('vendor:vendor_dashboard')
