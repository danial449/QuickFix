from django.urls import path
from .views import *

app_name = 'vendor' 

urlpatterns = [
    path("vendor-profile/", vendor_profile_detail_view, name="vendor_profile_detail_view"),
    path("vendor-profile/edit/", vendor_profile_edit_view, name="vendor_profile_edit"),
    path("add-service/", service_add_view, name="service_add_view"),
    path("my-services/<int:id>", my_service_detail_view, name="my_service_detail_view"),
    path("service-details/<int:service_id>", service_detail_view, name="service_detail_view"),
    path("my-services/delete/<int:service_id>", delete_service_view, name="delete_service_view"),
     path("vendor-dashboard/", vendor_dashboard_view, name="vendor_dashboard"),
    path("user-dashboard/", user_dashboard_view, name="user_dashboard"),
    path("book-service/<int:service_id>", book_service_view, name="book_service"),
    path('approve_booking/<int:booking_id>/<str:status>/', approve_booking_view, name='approve_booking'),
    path('delete-booking/<int:booking_id>', delete_booking_view, name='delete_booking'),
]