from .cart import Cart

# Creating context processors , to make work our cart on all the pages of site

def cart(request):
    #Return default data from cart
    return {'cart':Cart(request)}