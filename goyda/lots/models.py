from django.db import models
from users.models import User
from django.utils.translation import gettext_lazy as _
from category.models import Category
from core.validators import NameValidator, CityValidator
import uuid

class BaseLots(models.Model):
    
    def _get_default_category():
        return Category.objects.get(name='Another')
    
    ID = models.UUIDField(primary_key=True, db_index=True, default=uuid.uuid4)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_seller', verbose_name=_('seller'))
    buyer = models.ForeignKey(User, on_delete=models.SET_DEFAULT, null=True, default=None, blank=True, related_name='%(app_label)s_%(class)s_buyer', verbose_name=_('buyer'))
    title = models.CharField(_("lot name"), max_length=24, validators=[NameValidator(only_letters=False)])
    picture = models.ImageField(_("lot picture"), upload_to='lots_imgs', default='lots_imgs/default.jpg')
    category = models.ForeignKey(Category, on_delete=models.SET(_get_default_category), verbose_name=_('lot category'))
    start_price = models.PositiveIntegerField(_('the start price of the lot'))
    description = models.TextField(_('description of the lot'), blank=True, default=None)
    city = models.CharField(_('sellers city'), max_length=48, validators=[CityValidator()])
    date_of_placement = models.DateTimeField(_('date of placement'), auto_now_add=True)
    date_of_end = models.DateField(_('date of end'))

    def __str__(self):
        return self.title
    
    class Meta:
        abstract = True
    
    
class Lots(BaseLots):
    
    current_price = models.PositiveIntegerField(_('the current price of the lot'))
    
    class Meta:
        verbose_name = _('Lot')
        verbose_name_plural = _('Lots')
        ordering = ['-date_of_placement']
    

class ArchiveLots(BaseLots):
    
    finally_price = models.PositiveIntegerField(_('the finally price of the lot'))
    
    class Meta:
        verbose_name = _('Arhcive Lot')
        verbose_name_plural = _('Archive Lots')
        ordering = ['-date_of_placement']