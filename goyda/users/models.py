from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    
    first_name = models.CharField(max_length=48, verbose_name="First name")
    last_name = models.CharField(max_length=48, verbose_name="Last name")
    email = models.EmailField(verbose_name="User's email")
    
    city = models.CharField(max_length=48, verbose_name="The user's city")
    age = models.PositiveSmallIntegerField(verbose_name="User's age")
    purchases = models.PositiveSmallIntegerField(default=0, verbose_name="Purchases made by the user")
    sales = models.PositiveSmallIntegerField(default=0,verbose_name="Sales made by the user")
    balance = models.IntegerField(default=0, verbose_name="User's balance")
    about = models.TextField(blank=True, null=True, verbose_name='About the user')
    avatar = models.ImageField(upload_to='avatars', default='avatars/default.jpg')
    phone = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="The user's phone number")
