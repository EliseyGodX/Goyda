from django.db import models
from users.models import User
from lots.validators import Validator
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
        Validator.path(self.path)
        


class Lots(models.Model):
    
    class Meta:
        verbose_name = 'Lot'
        verbose_name_plural = 'Lots'
        get_latest_by = 'date_of_placement'
    
    ID = models.UUIDField(primary_key=True, db_index=True, default=uuid.uuid4)
    seller = models.ForeignKey(User, on_delete=models.SET(None), related_name='seller', verbose_name='Seller')
    buyer = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_DEFAULT, default=None, related_name='buyer', verbose_name='Buyer')
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