from django.contrib import admin
from .models import *

# The admin.py file is used to display your models in the Django admin panel
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)

