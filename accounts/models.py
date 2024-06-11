from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_admin = models.BooleanField('Is_admin' , default=False)
    is_customer = models.BooleanField('Is_customer' , default=False)
    is_vendor = models.BooleanField('Is_vendor' , default=False)

    CATAGORY_CHOICES = [('Punjab' ,'Punjab') ,('Sindh' ,'Sindh'),('Khyber Pakhtunkhwa','Khyber Pakhtunkhwa'),('Gilgit-Baltistan' ,'Gilgit-Baltistan') ,('Islamabad Capital Territory' ,'Islamabad Capital Territory'),('Balochistan','Balochistan'),]

    CATAGORY_EMP= [('Electrician' ,'Electrician'),('Plumber' ,'Plumber'),('Sweaper' ,'Sweaper'),('Carpenter' ,'Carpenter'),('Drain clean' ,'Drain clean'),('AC repair' ,'AC repair'),('Painting & Decorating' ,'Painting & Decorating'),]

    email = models.EmailField(null=True , unique=True)
    mobile_no = models.CharField(max_length=11 ,null=True, blank=True)
    address1 = models.CharField(max_length=200,default='abc')
    address2 = models.CharField(max_length=200,default='abc')
    city =  models.CharField(max_length=70 ,null=True, blank=True)
    province = models.CharField(choices=CATAGORY_CHOICES,default='Punjab', max_length=56)
    employee = models.CharField(choices=CATAGORY_EMP,default='none', max_length=100)
    cnic= models.CharField(max_length=13 ,null=True, blank=True)
    shop_reference = models.TextField(default='shop no address etc')
    vendor_image = models.ImageField(upload_to='vendor_profile_pics/')
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=200 ,blank=True, null=True)

    def __str__(self):
        return self.username