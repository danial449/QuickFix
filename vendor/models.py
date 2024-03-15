from django.db import models
from accounts.models import User
from django.utils import timezone

# Create your models here.

class Vendor_Profile(models.Model):
    CATAGORY_CHOICES = [('Punjab' ,'Punjab') ,('Sindh' ,'Sindh'),('Khyber Pakhtunkhwa','Khyber Pakhtunkhwa'),('Gilgit-Baltistan' ,'Gilgit-Baltistan') ,('Islamabad Capital Territory' ,'Islamabad Capital Territory'),('Balochistan','Balochistan'),]

    CATAGORY_EMP= [('Electrician' ,'Electrician'),('Plumber' ,'Plumber'),('Sweaper' ,'Sweaper'),('Carpenter' ,'Carpenter'),('Drain clean' ,'Drain clean'),('AC repair' ,'AC repair'),('Painting & Decorating' ,'Painting & Decorating'),]

    user = models.OneToOneField(User, on_delete=models.CASCADE ,  related_name='vendor_profile', blank=True, null=True)
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 30)
    username = models.CharField(max_length = 30)
    email = models.EmailField(null=True , unique=True)
    mobile_no = models.CharField(max_length=11 ,null=True, blank=True)
    address1 = models.CharField(max_length=200,default='None')
    address2 = models.CharField(max_length=200,default='None')
    city =  models.CharField(max_length=70 ,null=True, blank=True)
    province = models.CharField(choices=CATAGORY_CHOICES,default='None', max_length=56)
    employee = models.CharField(choices=CATAGORY_EMP,default='None', max_length=100)
    cnic= models.CharField(max_length=13 ,null=True, blank=True)
    shop_reference = models.TextField(default='None')
    vendor_image = models.ImageField(upload_to='vendor_profile_pics/')

    def __str__(self):
        return self.username

class Service_Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name 
    
class Service(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True ,null=True)
    service_title = models.CharField(max_length=50,null=True, blank=True)
    service_image = models.ImageField(upload_to='service_images/')
    categories=models.ForeignKey(Service_Category ,on_delete=models.CASCADE , blank=True ,null=True, related_name='category') 
    description = models.TextField(max_length=500,null=True, blank=True)

    def __str__(self):
        return str(self.service_title)
    
class Booking(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Booked', 'Booked'),
        ('Cancelled', 'Cancelled'),
    ]

    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(default=timezone.now)
    mobile_no = models.CharField(max_length=11, null=True, blank=True)
    email = models.EmailField(null=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    username = models.CharField(max_length=30, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.user.username} - {self.service.service_title}"
    
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE , related_name='feedback')
    feedback_text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now , null=True, blank=True)