from django.db import models
from users.models import User
from django.utils.translation import gettext as _
from lots.validators import Validator
import uuid

class Category(models.Model):
    
    name = models.CharField(_("category name"),max_length=48, unique=True)
    description = models.TextField(_("description"), blank=True, default=None)
    path = models.CharField(_("path to category"), max_length=48, validators=[Validator.path], unique=True)
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']
        
    def __str__(self):
        return self.name
        


class Lots(models.Model):
    
    ID = models.UUIDField(primary_key=True, db_index=True, default=uuid.uuid4)
    seller = models.ForeignKey(User, on_delete=models.SET(None), related_name='seller', verbose_name=_('seller'))
    buyer = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, blank=True, related_name='buyer', verbose_name=_('buyer'))
    title = models.CharField(_("lot name"), max_length=48, validators=[Validator.custom_name_onlyAlpha])
    picture = models.ImageField(_("lot picture"), upload_to='lots_imgs')
    category = models.ForeignKey(Category, on_delete=models.SET(Category.objects.get(name='Another')), verbose_name=_('lot category'))
    cost = models.PositiveIntegerField(_('the cost of the lot'))
    description = models.TextField(_('description of the lot'), blank=True, default=None)
    city = models.CharField(_('sellers city'), max_length=48, validators=[Validator.city])
    date_of_placement = models.DateTimeField(_('date of placement'), auto_now_add=True)
    date_of_end = models.DateField(_('date of end'))
    
    class Meta:
        verbose_name = 'Lot'
        verbose_name_plural = 'Lots'
        get_latest_by = 'date_of_placement'

    def __str__(self):
        return self.title