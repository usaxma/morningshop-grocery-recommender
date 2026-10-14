from django.contrib import admin

# Register your models here.

from .models import Products,Product_cats,Orders, OrderLineItems



admin.site.register(Products)
admin.site.register(Product_cats)
admin.site.register(Orders)
admin.site.register(OrderLineItems)