from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.


class Vendor_Profile_Admin(admin.ModelAdmin):
    list_display = ('id', 'first_name' , 'last_name', 'username' , 'email' , 'vendor_image')
admin.site.register(Vendor_Profile , Vendor_Profile_Admin)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ( 'id' , 'service_title' , 'service_image' , 'categories' , 'description')

admin.site.register(Service , ServiceAdmin)


class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_services')

    def display_services(self, obj):
        # Get the services related to this category
        services = Service.objects.filter(categories=obj)
        # Return a comma-separated list of service titles
        return ", ".join([service.service_title for service in services])

    # Set a more descriptive column header
    display_services.short_description = 'Services in Category'

admin.site.register(Service_Category , ServiceCategoryAdmin)


admin.site.register(Booking)
admin.site.register(Feedback)