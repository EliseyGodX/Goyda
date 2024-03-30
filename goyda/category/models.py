from django.db import models
from django.utils.translation import gettext_lazy as _
from core.validators import PathValidator

class Category(models.Model):
    
    name = models.CharField(_("category name"), max_length=48, unique=True)
    description = models.TextField(_("description"), blank=True, default=None)
    path = models.CharField(_("path to category"), max_length=48, validators=[PathValidator()], unique=True)
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']
        
    def __str__(self):
        return self.name
        
