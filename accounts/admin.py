from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.

class User_Admin(UserAdmin):
    list_display = ('id', 'first_name' , 'last_name', 'username', 'email')
    
    fieldsets = UserAdmin.fieldsets + (  # Include 'gender' in the 'Personal Information' section
        ('Other Information', {
            'fields': ('is_admin',
                       'is_vendor',
                       'is_customer',
                       'vendor_image',),
        }),
    )
admin.site.register(User , User_Admin)