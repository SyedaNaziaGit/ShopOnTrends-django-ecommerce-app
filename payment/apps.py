from django.apps import AppConfig


class PaymentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payment'
    
    #setting up paypal IPN signal - 
    # this ready function will be initiated whenevr the payment app is called or used- so hooks are imported here
    def ready(self):
        import payment.hooks
