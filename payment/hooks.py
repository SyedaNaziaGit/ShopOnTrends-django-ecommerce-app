from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from django.conf import settings
import time
from .models import Order

#craeting reciver decorator
@receiver(valid_ipn_received)
def paypal_payment_received(sender , **kwargs):
    time.sleep(10) # as paypal takes sometime to confirm the IPN data we add timer of 10s waiting period
    #Grab the info that paypal sends
    paypal_object = sender
    #Grab the invoice
    my_Invoice = str(paypal_object.invoice)
    #matching paypal invoice  to order invoice
    #lookup for the order
    my_Order = Order.objects.get(invoice = my_Invoice)
    #Check and record if the invoice was paid
    my_Order.paid = True
    #save order  to database the paid boolean field
    my_Order.save()
    