from django.db import models

from ecommerce.models import *


class Category(models.Model):
    catname=models.CharField(max_length=70)

class Product(models.Model):
    name=models.CharField(max_length=100)
    desc=models.CharField(max_length=200)
    price=models.DecimalField(decimal_places=2,max_digits=12)
    qty=models.IntegerField()
    pro_img=models.ImageField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    addedd_by=models.ForeignKey(userProfile, on_delete=models.CASCADE)
    dated=models.DateTimeField(auto_now=True)

    

