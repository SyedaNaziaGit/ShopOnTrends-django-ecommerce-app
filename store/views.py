from django.shortcuts import render,redirect
from .models import Product,Category,Profile
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm,UpdateUserForm,UpdatePasswordForm,UserInfoForm
from django.db.models import Q
import json
from shoppingcart.cart import Cart
from payment.forms import ShippingForm
from payment.models import ShippingAddress

#Get Individual Product
def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request,'product.html',{'product':product})

#Category Page
def category(request,foo):
    #Replace hypens with spaces
    foo = foo.replace("-"," ")
    #Grab the category from the url
    try:
        # Look up to the category
         category = Category.objects.get(name=foo)
         #get all the products in that category
         products =Product.objects.filter(category=category)
         return render(request,'category.html',{'products':products,'category':category})
    except:
        messages.success(request,"That Category doesn't exist")
        return redirect('home')

#category - summer page
def category_summary(request):
    categories = Category.objects.all()
    return render(request,'category_summary.html',{"categories":categories})

#Home Page- Get all products on home page.
def home(request):
    products = Product.objects.all()
    return render(request,'home.html',{'products':products})

#About Section
def about(request):
    return render(request,'about.html',{})

#Login User Section
def login_user(request):
    if request.method =="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            #Making the old cart persistat on login of the user
            current_user = Profile.objects.get(user__id = request.user.id)
            #getting the old cart saved from the Database of profile model
            saved_cart = current_user.old_cart
            #Converting str into dictionary using JSON
            if saved_cart:
                oldcart_dict = json.loads(saved_cart)
                #add this dict to session
                cart = Cart(request)
                #add items from dict by looping 
                for key,value in oldcart_dict.items():
                    cart.db_add(product=key,quantity=value)
                
            messages.success(request, "You have Logged In Successfully")
            return redirect('home')
        else:
            messages.success(request, "There was an error please try again")
            return redirect('login')
    else:    
        return render(request,"login.html",{})

#Logout User Section
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out successfully..")
    return redirect('home')

#Register User Section
def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password2']
            # Log In to user account
            user = authenticate(username= username, password=password)
            login(request,user)
            messages.success(request, "You have Registered Successfully!!")
            return redirect('update_user')
        else:
            messages.success(request,"Oops, there was a problem, Try Again!!")
            return redirect('register')
    else:
        return render(request,"register.html",{'form':form})
    
#Update User information
def update_user(request):
    #if user has logged in only then update the info
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance =current_user)
        if user_form.is_valid():
            user_form.save()
            login(request,request.user)
            messages.success(request,"Your  Profile has been Updated")
            return redirect('home')
        return render(request,"update_user.html",{"user_form":user_form})
    else:
        messages.success(request,"You must be logged into access the Update Profile")
        return redirect('home')

#Update user Information
def update_info(request):
    #if user has logged in only then update the info
    if request.user.is_authenticated:
        #current user tht is logged in
        current_user = Profile.objects.get(user__id = request.user.id)
        #shipping user from the shipping address
        shipping_user = ShippingAddress.objects.get(id = request.user.id)
        #get original  User form
        form = UserInfoForm(request.POST or None, instance = current_user)
        #get users shipping form
        shipping_form = ShippingForm(request.POST or None , instance = shipping_user)
        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request,"Your  Information has been Updated")
            return redirect('home')
        return render(request,"update_info.html",{"form":form,"shipping_form":shipping_form})
    else:
        messages.success(request,"You must be logged into access the Update Information")
        return redirect('home')


#Update User Password
def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        #If Form is filled
        if request.method == "POST":
            form = UpdatePasswordForm(current_user,request.POST)
            # is the form valid
            if form.is_valid():
                form.save()
                messages.success(request,"Your Password has been Updated..")
                login(request,current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request,error)
                return redirect('update_password')
        else:
            form = UpdatePasswordForm(current_user)
    else:
        messages.success(request,"You must be logged in to update password")
    return render(request,"update_password.html",{'form':form})

#searching the product 
def search(request):
    #To check if they filled out the form
    if request.method == "POST":
        searched = request.POST['searched']
        #Query the products from database Model - to do multiple queries we use Q from db.models
        searched = Product.objects.filter(Q(name__icontains=searched)| Q(description__icontains = searched))
        #Test if Null
        if not searched:
            messages.success(request,"Sorry that Product doesn't exists .. Please Try Again..")
            return render(request,"search.html",{})
        else:
            return render(request,"search.html",{"searched":searched})
    else:
        return render(request,"search.html",{})