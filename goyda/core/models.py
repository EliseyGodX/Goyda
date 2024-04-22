from django.db import models
from django.utils.translation import gettext_lazy as _


class Country(models.Model):
    
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=128, db_index=True)
    
    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')
        db_table = 'country'
        
    def __str__(self):
        return self.name
    
    
class Region(models.Model):
    
    id = models.BigIntegerField(primary_key=True)
    country = models.ForeignKey('core.Country', on_delete=models.PROTECT, db_index=True)
    name = models.CharField(max_length=128, db_index=True)
    
    class Meta:
        verbose_name = _('Region')
        verbose_name_plural = _('Regions')
        db_table = 'region'
        
    def __str__(self):
        return self.name
    
    @property
    def full_address(self):
        return f'{self.country}, {self.name}'
        

class City(models.Model):
    
    id = models.BigIntegerField(primary_key=True)
    region = models.ForeignKey('core.Region', on_delete=models.PROTECT, db_index=True)
    name = models.CharField(max_length=128, db_index=True)
    
    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')
        db_table = 'city'
        
    def __str__(self):
        return self.name
    
    @property
    def full_address(self):
        return f'{self.region.full_address}, {self.name}'