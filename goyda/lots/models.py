from django.db import models
import uuid

class Category(models.Model):
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    name = models.CharField(max_length=48, verbose_name='category name')
    description = models.TextField(verbose_name='Description')
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return {'name': self.name,
                'description': self.description}
        

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
    
    id_ = models.UUIDField(primary_key=True, db_index=True, default=uuid.uuid4)
    name = models.CharField(max_lenght=48, verbose_name='Lot name')
    picture = models.ImageField(upload_to='/lots')
    category = models.ForeignKey(Category, on_delete=models.SET('other'))
    cost = models.PositiveIntegerField(verbose_name='The cost of the lot')
    description = models.TextField(verbose_name='Description of the lot')
    city = models.CharField(max_lenght=48, verbose_name='Sellers City')
    date_of_placement = models.DateTimeField(auto_now_add=True, verbose_name='Date of placement')
    date_of_end = models.DateField(verbose_name='Date of placement')


    def __str__(self):
        return self.name