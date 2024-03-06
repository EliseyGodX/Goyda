from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

import uuid

class Category(models.Model):
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    name = models.CharField(max_length=48, verbose_name='Category name', unique=True)
    description = models.TextField(null=True, default=None, verbose_name='Description')
    path = models.CharField(max_length=48, verbose_name='Path name', unique=True)
    
    def __str__(self):
        return self.name
    
    def clean(self):
        super().clean()
        if self.path and not self.path.endswith('/'):
            raise ValidationError('Path must end with "/"')
        

class Users(models.Model):
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['user']
        
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    city = models.CharField(max_length=48, verbose_name="The user's city")
    age = models.PositiveSmallIntegerField(verbose_name="User's age")
    purchases = models.PositiveSmallIntegerField(verbose_name="Purchases made by the user")
    sales = models.PositiveSmallIntegerField(verbose_name="Sales made by the user")
    balance = models.IntegerField(verbose_name="User's balance")
    about = models.TextField(blank=True, default=None, verbose_name='About the user')
    avatar = models.ImageField(upload_to='avatars')
    phone = models.PositiveSmallIntegerField(verbose_name="The user's phone number", unique=True)
    
    def __str__(self):
        return self.user.username
    

class Lots(models.Model):
    
    class Meta:
        verbose_name = 'Lot'
        verbose_name_plural = 'Lots'
        get_latest_by = 'date_of_placement'
    
    ID = models.UUIDField(primary_key=True, db_index=True, default=uuid.uuid4)
    seller = models.ForeignKey(Users, on_delete=models.SET(None), related_name='seller',verbose_name='Seller')
    buyer = models.ForeignKey(Users, null=True, on_delete=models.SET_DEFAULT, default=None, related_name='buyer', verbose_name='Buyer')
    title = models.CharField(max_length=48, verbose_name='Lot name')
    picture = models.ImageField(upload_to='lots_imgs')
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_DEFAULT, default=None, verbose_name='lot category')
    cost = models.PositiveIntegerField(verbose_name='The cost of the lot')
    description = models.TextField(blank=True, default=None, verbose_name='Description of the lot')
    city = models.CharField(max_length=48, verbose_name='Sellers City')
    date_of_placement = models.DateTimeField(auto_now_add=True, verbose_name='Date of placement')
    date_of_end = models.DateField(verbose_name='Date of end')

    def __str__(self):
        return self.title