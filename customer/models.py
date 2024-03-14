from django.db import models
from accounts.models import User
# Create our models here.

class ContactUs(models.Model):
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 20)
    email = models.EmailField(null=False , unique=False)
    message = models.TextField(max_length = 500)

    def __str__(self):
        return self.message

class User_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE , blank=True, null=True)
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 30)
    username = models.CharField(max_length = 30)
    email = models.EmailField(null=True , unique=True)
    mobile_no = models.CharField(max_length=11, null=True, blank=True)
    user_image = models.ImageField(upload_to='profile_pics/' , null=True , blank=True)

    def __str__(self):
        return self.username