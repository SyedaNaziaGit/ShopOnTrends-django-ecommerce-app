from store.models import Product,Profile

class Cart():
    def __init__(self,request):
        self.session = request.session
        #Get request for user persistance
        self.request = request
        # Get the current session key if it exists
        cart = self.session.get('session_key')
        # If the user is new , then there is no session key , so create one
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        
        #Make sure cart is available on all the pages of the website
        self.cart=cart
    
    def add(self,product,quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        #Logic to check if prod is added already in cart
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id]={'price':str(product.price)}
            self.cart[product_id]=int(product_qty)
        self.session.modified = True
        #persistance of user - for user logged in
        if self.request.user.is_authenticated:
            #get the current user profilr
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #converting it to str to store as persistant var
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            #save the carty to profile model
            current_user.update(old_cart = str(carty))
    
    #to get the number of items in cart
    def __len__(self):
        return len(self.cart)
    
    #to get the products in cart
    def get_prods(self):
        #get product ids from cart
        product_ids = self.cart.keys()
        #use ids to lookup  products in database model
        products =Product.objects.filter(id__in =product_ids)
        #return all the lookedup products from database on cart
        return products
    
    #to get the quantity of products in the cart summary
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    #update cart
    def update(self,product,quantity):
        product_id = str(product)
        product_qty = int(quantity)
        #get Cart
        ourcart = self.cart
        # Update dictonary cart
        ourcart[product_id] = product_qty
        self.session.modified = True
        #persistance of user - for user logged in
        if self.request.user.is_authenticated:
            #get the current user profilr
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #converting it to str to store as persistant var
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            #save the carty to profile model
            current_user.update(old_cart = str(carty))
        updatedcart = self.cart
        return updatedcart
    
    #deleting the product with the productid 
    def delete(self,product):
        product_id = str(product)# we have created a session as str
        #delete  product from the cart
        if product_id in self.cart:
            del self.cart[product_id]
        # as we have deleted the product we are updating the session
        self.session.modified = True 
        #persistance of user - for user logged in
        if self.request.user.is_authenticated:
            #get the current user profilr
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #converting it to str to store as persistant var
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            #save the carty to profile model
            current_user.update(old_cart = str(carty))
    
    #to get the sum of the products in the cart
    def cart_total(self):
        #get the cart - its a dict of prodid as key and num of items as val
        #get productids
        product_ids = self.cart.keys()
        #lookup those keys in product database model
        products = Product.objects.filter(id__in = product_ids)
        #get quantities
        quantities = self.cart
        total = 0
        #adding product prices
        for key,value in quantities.items():
            key=int(key)#convert str key into int
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price*value)
                    else:
                        total = total + (product.price*value)
        return total
    
    #add to db and save on dict for login persistance
    def db_add(self,product,quantity):
        product_id = str(product)
        product_qty = str(quantity)
        #Logic to check if prod is added already in cart
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id]={'price':str(product.price)}
            self.cart[product_id]=int(product_qty)
        self.session.modified = True
        #persistance of user - for user logged in
        if self.request.user.is_authenticated:
            #get the current user profilr
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #converting it to str to store as persistant var
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            #save the carty to profile model
            current_user.update(old_cart = str(carty))