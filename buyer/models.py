
from django.db import models

from seller.models import *
from ecommerce.models import *

from buyer.models import *

class Cart(models.Model):

    class Meta():
        # It will make (Product (coloumn) AND User Column as uinique together (At a time both record should not be same))
        unique_together=('user','product')

    user=models.ForeignKey(userProfile, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)

class orders(models.Model):
    order_id=models.CharField(max_length=100) # OID_DATE(DDMMYYYY)_RandomNumber
    order_date=models.DateField(auto_now=True)
    total_amt=models.DecimalField(max_digits=10,decimal_places=3)
    amt_status=models.IntegerField(default=0) # 0 Unpaid
    #order_status=models.IntegerField(default=0) # 0 for Placed
    placed_by=models.ForeignKey(userProfile, on_delete=models.CASCADE)
    
    Address=models.ForeignKey('AddressDetails', on_delete=models.CASCADE)
    
class OrderProduct(models.Model):
    order=models.ForeignKey(orders, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    qty=models.IntegerField()
    status=models.IntegerField(default=0)

class AddressDetails(models.Model):
    Address_line1=models.CharField(max_length=100)
    Address_line2=models.CharField(max_length=100)
    pincode=models.IntegerField()
    city=models.CharField(max_length=100)
    landmark=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    mobile=models.CharField(max_length=13)
    user=models.ForeignKey(userProfile,on_delete=models.CASCADE)
   