from django.shortcuts import render,redirect
from django.contrib import messages
from shoppingcart.cart import Cart
from payment.forms import ShippingForm,PaymentForm
from payment.models import ShippingAddress,Order,OrderItems
from django.contrib.auth.models import User
from store.models import Product,Profile
from datetime import datetime
#importing paypal things here
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
#for creating unique user ids for duplicate orders use uuid
import uuid


#order on link
def orders(request,pk):
    if request.user.is_authenticated and request.user.is_superuser:
        #get the order
        order = Order.objects.get(id=pk)
        #Get the order items
        items = OrderItems.objects.filter(order=pk)
        now = datetime.now()
        if request.POST:
            status = request.POST['shipping_status']
            #Check if status is true or false
            if status == "true":
                #get the order
                order = Order.objects.filter(id=pk)
                #update status
                order.update(shipped = True,date_shipped = now)
            else:
                #get the order
                order = Order.objects.filter(id=pk)
                #update status
                order.update(shipped = False,date_shipped = now)
            messages.success(request,"Shipping Status Updated")
            return redirect("home")
        return render(request,"payment/orders.html",{"order":order,"items":items})
    else:
        messages.success(request,"Access Denied")
        return render(request,"",{})
    
#Shipped dashboard
def shipped_dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped = True)
        now = datetime.now()
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            order = Order.objects.filter(id=num)
            #update status
            order.update(shipped = False,date_shipped = now)
            messages.success(request,"Shipping Status Updated")
            return redirect("home")
        return render(request,"payment/shipped_dashboard.html",{"orders":orders})
    else:
        messages.success(request,"Access denied")
        return redirect("home")
    

#Not shipped Dashboard
def not_shipped_dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped = False)
        now = datetime.now()
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            #get order
            order = Order.objects.filter(id=num)
            #update status
            order.update(shipped = True,date_shipped = now)
            messages.success(request,"Shipping Status Updated")
            return redirect("home")
        return render(request,"payment/not_shipped_dashboard.html",{"orders":orders})
    else:
        messages.success(request,"Access Denied")
        return redirect("home")

#Processing Order
def process_order(request):
    if request.POST:
        #get the cart session price details
        cart = Cart(request)
        cart_products = cart.get_prods()
        #to retain the quantity of products
        quantities = cart.get_quants()
        #cart total amoungt update
        totals = cart.cart_total()
        
        #get billing info
        payment_form = PaymentForm(request.POST or None)
        #get shipping session  from the shipping session saved in billing info
        my_shipping = request.session.get('my_shipping')
        #Gathering order info
        full_name  = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        #creating shipping concating address from session myshipping
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_country']}\n"
        amount_paid = totals
        
        
        #Create an order
        if request.user.is_authenticated:
            user = request.user
            #creating an order
            create_order = Order(user = user,full_name = full_name,email=email,shipping_address=shipping_address,amount_paid=amount_paid)
            create_order.save()
            #add order items of the Order Placed with id for each models created by django
            #get the order id from primary key
            order_id = create_order.pk
            #get product info from cart
            for product in cart_products:
                product_id = product.id
                #product price or sale price
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                #get the quantity
                for key,value in quantities.items():
                    if int(key) == product_id:
                        quantity = value
                        #create order items
                        create_order_item = OrderItems(order_id=order_id,user=user,product_id=product_id,quantity=quantity,price=price)
                        create_order_item.save()
            #Delete our cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    #delete the session key and the data in that key with the del -making the shopping cart empty
                    del request.session[key]
            #Delete  Cart from the database(oldcart field)
            current_user = Profile.objects.filter(user__id = request.user.id)
            #Delete shopping in database
            current_user.update(old_cart = "")
            messages.success(request,"Ordered Placed..")
            return redirect("home")
        else:
            #not logged
            create_order = Order(user = user,full_name = full_name,email=email,shipping_address=shipping_address,amount_paid=amount_paid)
            create_order.save()
            #add order items of the Order Placed with id for each models created by django
            #get the order id from primary key
            order_id = create_order.pk
            #get product info from cart
            for product in cart_products:
                product_id = product.id
                #product price or sale price
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                #get the quantity
                for key,value in quantities.items():
                    if int(key) == product_id:
                        quantity = value
                        #create order items
                        create_order_item = OrderItems(order_id=order_id,product_id=product_id,quantity=quantity,price=price)
                        create_order_item.save()
            #Delete our cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    #delete the session key and the data in that key with the del -making the shopping cart empty
                    del request.session[key]
            messages.success(request,"Ordered Placed..")
            return redirect("home")      
    else:
        messages.success(request,"Access Denied..")
        return redirect("home")

def payment_success(request):
    #delete the browser cart
    #get the cart first from the browser
    cart = Cart(request)
    cart_products = cart.get_prods()
    #to retain the quantity of products
    quantities = cart.get_quants()
    #cart total amoungt update
    totals = cart.cart_total()
    
    #Delete our cart
    for key in list(request.session.keys()):
        if key == "session_key":
            #delete the session key and the data in that key with the del -making the shopping cart empty
            del request.session[key]
    return render(request,'payment/payment_success.html',{})

def payment_failed(request):
    return render(request,'payment/payment_failed.html',{})

def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    #to retain the quantity of products
    quantities = cart.get_quants()
    #cart total amoungt update
    totals = cart.cart_total()
    #checking if the user is logged in or not and always need not that the user is logged 
    if request.user.is_authenticated:
        #Checkout as Login User
        shipping_user = ShippingAddress.objects.get(id = request.user.id)
        shipping_form = ShippingForm(request.POST or None , instance = shipping_user)
        return render(request,'payment/checkout.html',{"cart_products":cart_products,"quantities":quantities,"totals":totals,"shipping_form":shipping_form})
    else:
        #Checkout as Guest
        shipping_user = ShippingAddress.objects.get(id = request.user.id)
        shipping_form = ShippingForm(request.POST or None , instance = shipping_user)
        return render(request,'payment/checkout.html',{"cart_products":cart_products,"quantities":quantities,"totals":totals,"shipping_form":shipping_form})
    
#Billing Information 
def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods()
        #to retain the quantity of products
        quantities = cart.get_quants()
        #cart total amoungt update
        totals = cart.cart_total()
        
        #Create a session with the shipping info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping
        
        #get tehe host 
        host = request.get_host()
        #Creating Invoice num
        my_Invoice = str(uuid.uuid4())
        #Creating Payment - Paypal things here
        paypal_dict = {
            'business' : settings.PAYPAL_RECEIVER_EMAIL,
            'amount' :totals,
            'item_name' : 'Book Order',
            'no_shipping':'2',
            'invoice' : my_Invoice,
            'currency_code':'USD',
            'notify_url':'https://{}{}'.format(host,reverse('paypal-ipn')),
            'return_url':'https://{}{}'.format(host,reverse('payment_success')),
            'cancel_return':'https://{}{}'.format(host,reverse('payment_failed')),
        }
        #Creating Paypal Form button here
        paypal_form = PayPalPaymentsForm(initial =paypal_dict)
        
        #Gathering order info
        full_name  = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        #creating shipping concating address from session myshipping
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_country']}\n"
        amount_paid = totals
        
        #Check to see if user is logged in
        if request.user.is_authenticated:
            #Get the Billing Information from the payment form
            billing_form = PaymentForm()    
                
            user = request.user
            #creating an order
            create_order = Order(user = user,full_name = full_name,email = email,shipping_address = shipping_address,amount_paid = amount_paid,invoice = my_Invoice)
            create_order.save()
            #add order items of the Order Placed with id for each models created by django
            #get the order id from primary key
            order_id = create_order.pk
            #get product info from cart
            for product in cart_products:
                product_id = product.id
                #product price or sale price
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                #get the quantity
                for key,value in quantities.items():
                    if int(key) == product_id:
                        quantity = value
                        #create order items
                        create_order_item = OrderItems(order_id=order_id,user=user,product_id=product_id,quantity=quantity,price=price)
                        create_order_item.save()
            messages.success(request,"Ordered Placed..")
            return render(request,"payment/billing_info.html",{"shipping_info":request.POST,"cart_products":cart_products,"quantities":quantities,"totals":totals,"billing_form":billing_form,"paypal_form":paypal_form})
        else:
            #not logged
            create_order = Order(user = user,full_name = full_name,email = email,shipping_address = shipping_address,amount_paid = amount_paid,invoice=my_Invoice)
            create_order.save()
            #add order items of the Order Placed with id for each models created by django
            #get the order id from primary key
            order_id = create_order.pk
            #get product info from cart
            for product in cart_products:
                product_id = product.id
                #product price or sale price
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                #get the quantity
                for key,value in quantities.items():
                    if int(key) == product_id:
                        quantity = value
                        #create order items
                        create_order_item = OrderItems(order_id=order_id,product_id=product_id,quantity=quantity,price=price)
                        create_order_item.save()
            return render(request,"payment/billing_info.html",{"shipping_info":request.POST,"cart_products":cart_products,"quantities":quantities,"totals":totals,"billing_form":billing_form,"paypal_form":paypal_form})
    else:
        messages.success(request,"Access Denied")
        return redirect("home")