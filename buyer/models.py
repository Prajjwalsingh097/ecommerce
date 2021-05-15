from django.db import models

from seller.models import *
from ecommerce.models import *

class Cart(models.Model):

    class Meta():
        # It will make (Product (coloumn) AND User Column as uinique together (At a time both record should not be same))
        unique_together=('user','product')

    user=models.ForeignKey(userProfile, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    