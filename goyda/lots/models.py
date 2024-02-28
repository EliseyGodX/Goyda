from django.db import models
import uuid

class Category(models.Model):
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    name = models.CharField(max_length=48, verbose_name='category name', unique=True)
    description = models.TextField(null=True, default=None, verbose_name='Description')
    
    
    def __str__(self):
        return self.name
        

class Users(models.Model):
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['surname']
        
    ID = models.UUIDField(primary_key=True, db_index=True, default=uuid.uuid4)
    name = models.CharField(max_length=48, verbose_name='Username')
    surname = models.CharField(max_length=48, verbose_name='User surname')
    city = models.CharField(max_length=48, verbose_name="The user's city")
    age = models.PositiveSmallIntegerField(verbose_name="User's age")
    purchases = models.PositiveSmallIntegerField(verbose_name="Purchases made by the user")
    sales = models.PositiveSmallIntegerField(verbose_name="Sales made by the user")
    date_of_registration = models.DateTimeField(auto_now_add=True, verbose_name='Date of user registration')
    balance = models.IntegerField(verbose_name="User's balance")
    about = models.TextField(null=True, default=None, verbose_name='About the user')
    avatar = models.ImageField(upload_to=r'goyda\lots\templates\lots\avatars')
    email = models.EmailField(verbose_name="User's email address", unique=True)
    phone = models.PositiveSmallIntegerField(verbose_name="The user's phone number", unique=True)
    banned = models.BooleanField(default=False, verbose_name='The user is banned')
    
    def __str__(self):
        return self.name
    

class Lots(models.Model):
    
    class Meta:
        verbose_name = 'Lot'
        verbose_name_plural = 'Lots'
        get_latest_by = 'date_of_placement'
        
    
    # CATEGORIES = {
    #     'transport': Category(name='Means of transportation', description=''),
    #     'realty': Category('Realty', description=''),
    #     'personal': Category('Personal thing', description=''),
    #     'home': Category('For home', description=''),
    #     'accessories': Category('Accessories', description=''),
    #     'electronics': Category('Electronics', description=''),
    #     'hobbies': Category('Hobbies and recreation', description=''),
    #     'animals': Category('Animals', description=''),
    #     'other': Category('Another category', description='')
    # }
    # for category in CATEGORIES: category.save()
    
    ID = models.UUIDField(primary_key=True, db_index=True, default=uuid.uuid4)
    seller = models.ForeignKey(Users, on_delete=models.SET(None), related_name='seller',verbose_name='Seller')
    buyer = models.ForeignKey(Users, null=True, on_delete=models.SET_DEFAULT, default=None, related_name='buyer', verbose_name='Buyer')
    title = models.CharField(max_length=48, verbose_name='Lot name')
    picture = models.ImageField(upload_to=r'goyda\lots\templates\lots\img_lots')
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_DEFAULT, default=None, verbose_name='lot category')
    cost = models.PositiveIntegerField(verbose_name='The cost of the lot')
    description = models.TextField(verbose_name='Description of the lot')
    city = models.CharField(max_length=48, verbose_name='Sellers City')
    date_of_placement = models.DateTimeField(auto_now_add=True, verbose_name='Date of placement')
    date_of_end = models.DateField(verbose_name='Date of placement')

    def __str__(self):
        return self.title