from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
        
    city = models.CharField(max_length=48, verbose_name="The user's city")
    age = models.PositiveSmallIntegerField(verbose_name="User's age")
    purchases = models.PositiveSmallIntegerField(verbose_name="Purchases made by the user", default=0)
    sales = models.PositiveSmallIntegerField(verbose_name="Sales made by the user", default=0)
    balance = models.IntegerField(verbose_name="User's balance", default=0)
    about = models.TextField(blank=True, null=True, verbose_name='About the user')
    avatar = models.ImageField(upload_to='avatars')
    phone = models.PositiveSmallIntegerField(verbose_name="The user's phone number", blank=True, null=True)
