from django.db import models
from django.contrib.auth.models import AbstractUser
from lots.validators import Validator

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
    phone = models.CharField(blank=True, null=True, max_length=19, verbose_name="The user's phone number")

    def clean(self):
        Validator.custom_name_onlyAlpha(self.first_name, 'first name')
        Validator.custom_name_onlyAlpha(self.last_name, 'last name')
        Validator.city(self.city)
        Validator.age(self.age)
        if self.phone is not None:
            Validator.phone_number(self.phone)