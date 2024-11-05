from django.shortcuts import render,get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages

#Cart summary here
def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    #to retain the quantity of products
    quantities = cart.get_quants()
    #cart total amoungt update
    totals = cart.cart_total()
    return render(request,'cart_summary.html',{"cart_products":cart_products,"quantities":quantities,"totals":totals})

#Add to Cart 
def cart_add(request):
    #Get the cart here
    cart = Cart(request)
    #test the post
    if request.POST.get('action')=="post":
        # get the items
        product_id = int(request.POST.get('product_id'))
        #getting the num of items selected in the cart
        product_qty = int(request.POST.get('product_qty'))
        #lookup for the product in Database
        product = get_object_or_404(Product,id=product_id)
        # Save this to the session
        cart.add(product=product,quantity=product_qty)
        #get the cart quantity from the cart
        cart_quantity = cart.__len__()
        #Return the JSON Response
        #response = JsonResponse({'Product Name':product.name})
        response= JsonResponse({'qty':cart_quantity})
        messages.success(request, "Product Added to Cart!")
        return response
    
#Delete Item From Cart 
def cart_delete(request):
    # get the instace of cart
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        #get product id which needs to be deleted
        product_id = int(request.POST.get('product_id'))
        #call the delete function from the cart utility
        cart.delete(product_id)
        response = JsonResponse({'product':product_id})
        messages.success(request, "Product Deleted From Cart..")
        return response        

#Update Item to Cart 
def cart_update(request):
    #get instance of the cart
    cart = Cart(request)
    #test a POST
    if request.POST.get('action') == "post":
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        #cart update
        cart.update(product = product_id,quantity= product_qty)
        response = JsonResponse({'qty':product_qty})
        messages.success(request, "Updated Cart Successfully")
        return response
    #return redirect('cart_summary')

