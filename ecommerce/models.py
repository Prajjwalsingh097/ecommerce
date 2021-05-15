from django.db import models
from django.contrib.auth.models import User

class userProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    userType=models.CharField(max_length=70)
    mobile=models.CharField(max_length=20)
    address=models.CharField(max_length=70)
    username=models.CharField(max_length=70)
