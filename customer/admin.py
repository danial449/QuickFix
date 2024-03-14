from django.contrib import admin
from .models import *
# Register your models here.

class Contact_Us_Admin(admin.ModelAdmin):
    list_display = ('id','first_name' , 'last_name' , 'email' , 'subject', 'message')
admin.site.register(ContactUs , Contact_Us_Admin)

class User_Profile_Admin(admin.ModelAdmin):
    list_display = ('id', 'user','first_name' , 'last_name' , 'email' , 'user_image')
admin.site.register(User_Profile , User_Profile_Admin)