from django.contrib import admin
from .models import ShippingAddress,Order,OrderItems
from django.contrib.auth.models import User

admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItems)

#put the items of orderitems in the order placed with help of inline in admin
#create an order item inline
class OrderItemsInline(admin.StackedInline):
    model = OrderItems
    extra = 0

#Extend order model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ['date_ordered']
    fields = ["user","full_name","email","shipping_address","amount_paid","date_ordered","shipped","date_shipped","invoice","paid"]
    inlines = [OrderItemsInline]
    
#un-register
admin.site.unregister(Order)
#re-register our order with order admin newly created
admin.site.register(Order,OrderAdmin)
