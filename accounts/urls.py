from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path("vendor-register/", vendor_register_view, name="vendor_register_view"),
    path("register/", user_register_view, name="user_register_view"),
    path("login/", user_login_view, name="user_login_view"),
    path("logout/", user_logout_view, name="user_logout_view"),
]
