from django.core.validators import validate_unicode_slug
from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    
    name = models.CharField(_("category name"), max_length=48, unique=True)
    description = models.TextField(_("description"), blank=True, default=None)
    slug = models.CharField(_("path to category"), db_index=True, max_length=48, validators=[validate_unicode_slug], unique=True)
    
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['name']
        
    def __str__(self):
        return self.name
        
