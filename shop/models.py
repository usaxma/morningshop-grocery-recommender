from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import User
# Create your models here.
from user_control.models import UsersAccount

class Product_cats(models.Model):

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.name

class Products(models.Model):
    name = models.CharField("Product Name",max_length=255)
    featured_img_url = models.CharField("Featured Image to use on the display JSON Stringified",max_length=500, blank=True)
    extra_img_urls = models.CharField("Extra Images JSON Stringified", max_length=2000, blank=True)
    description = models.CharField("Product Description",max_length=2000,blank=True)
    category = models.ManyToManyField(Product_cats,blank=True)
    price = models.IntegerField()
    stock = models.IntegerField()
    rating = models.IntegerField(null=True)

class Rating(models.Model):
    user_id = models.IntegerField(default=0)
    product_id = models.CharField(max_length=255,default=0)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.name




class Orders(models.Model):
    customer_id = models.CharField(max_length=255)
    shipping_name = models.CharField(max_length=255,default="")
    shipping_phone = models.CharField(max_length=100,default="")
    shipping_email = models.CharField(max_length=255, default="")
    shipping_addr_1 =   models.CharField(max_length=255, default="")
    shipping_addr_2 =   models.CharField(max_length=255,default="")
    shipping_city = models.CharField(max_length=100,default="")
    shipping_country = models.CharField(max_length=100,default="")
    shipping_district = models.CharField(max_length=100, default="")
    shipping_zip = models.CharField(max_length=50, default="")
    shipping_status = models.IntegerField(default=0)
    orderCustomer = models.ForeignKey(UsersAccount, on_delete=models.CASCADE,default=None,blank=True)
    total = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True,blank=True)


class OrderLineItems(models.Model):
    order_id = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products,on_delete=models.CASCADE)
    quantity = models.CharField(max_length=30)






