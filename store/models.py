from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save

#Create Customer Prodile
class Profile(models.Model):
    #associating this prodile model with the django User model - models.Cascade will delete the associated or related model to it
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User,auto_now=True)
    phone = models.CharField(max_length=10,blank=True)
    address1 = models.CharField(max_length=200,blank=True)
    address2 = models.CharField(max_length=200,blank=True)
    city =  models.CharField(max_length=50,blank=True)
    state = models.CharField(max_length=50,blank=True)
    zipcode = models.CharField(max_length=15,blank=True)
    country = models.CharField(max_length=50,blank=True)
    old_cart = models.CharField(max_length=200,blank=True,null=True)
    
    #for admin lookup
    def __str__(self):
        return self.user.username

#Create a user profile by default when user signsup -instance here is the obj created when they are registering or all info obj
def create_profile(sender,instance,created,**kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        
#Automate the profile
post_save.connect(create_profile,sender=User)

#Categories Of Products
class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "categories"
    
#Customers 
class Customer(models.Model):   
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.firstname} {self.lastname}'

    class Meta:
        verbose_name_plural = "customers"
        
#All products
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0,decimal_places=2,max_digits=6)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,default =1)
    description = models.CharField(max_length=350,default='',blank=True,null = True)
    image = models.ImageField(upload_to='uploads/product')
    #Add sale stuff
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0,decimal_places=2,max_digits=6)
    
    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        verbose_name_plural = "products"
    
#Orders of customers model
class Order(models.Model):  
    product = models.ForeignKey(Product, on_delete=models.CASCADE,default =1)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,default =1)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=250, default='',blank=True)
    phone = models.CharField(max_length=10, default='', blank=True)
    date = models.DateField(default=datetime.date.today())
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.product}'
    
    class Meta:
        verbose_name_plural = "orders"