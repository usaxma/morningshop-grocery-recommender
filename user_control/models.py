from django.db import models
from django.contrib.auth.models import User
#  Admin and Custermer user



class UsersAccount(models.Model):
    mainUser = models.ForeignKey(User,on_delete=models.CASCADE)
    Gender = models.CharField(max_length=255,default="")
    DateOfBirth = models.DateField()
    Phone = models.CharField(max_length=50,default="")
    Address =   models.CharField(max_length=255, default="")
    City = models.CharField(max_length=100,default="")
    Country = models.CharField(max_length=100,default="")
    zipCode = models.CharField(max_length=50, default="")
    account_type = models.CharField(max_length=50, default="")
    status = models.IntegerField(default=0)




