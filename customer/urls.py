from django.urls import path
from .views import *

app_name = 'customer'

urlpatterns = [
    path("", home_view, name="home"),
    path("about/", about_us_view, name="about"),
    path("contact/", contact_us_view, name="contact"),
    path("contact/", contact_us_view, name="contact_us_view"),
    path("about/", about_us_view, name="about_us_view"),
    path("service/", service_view, name="service_view"),
    path("profile/", user_profile_detail_view, name="user_profile_detail_view"),
    path("profile/edit/", user_profile_edit_view, name="user_profile_edit_view"),
]
