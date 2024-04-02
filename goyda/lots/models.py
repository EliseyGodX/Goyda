from django.db import models
from users.models import User
from django.utils.translation import gettext_lazy as _
from category.models import Category
from core.validators import NameValidator, CityValidator
import uuid

class Lots(models.Model):
    
    def _get_default_category():
        return Category.objects.get(name='Another')
    
    ID = models.UUIDField(primary_key=True, db_index=True, default=uuid.uuid4)
    seller = models.ForeignKey(User, on_delete=models.SET(None), related_name='seller', verbose_name=_('seller'))
    buyer = models.ForeignKey(User, on_delete=models.SET_DEFAULT, null=True, default=None, blank=True, related_name='buyer', verbose_name=_('buyer'))
    title = models.CharField(_("lot name"), max_length=24, validators=[NameValidator(only_letters=False)])
    picture = models.ImageField(_("lot picture"), upload_to='lots_imgs')
    category = models.ForeignKey(Category, on_delete=models.SET(_get_default_category), verbose_name=_('lot category'))
    price = models.PositiveIntegerField(_('the price of the lot'))
    description = models.TextField(_('description of the lot'), blank=True, default=None)
    city = models.CharField(_('sellers city'), max_length=48, validators=[CityValidator()])
    date_of_placement = models.DateTimeField(_('date of placement'), auto_now_add=True)
    date_of_end = models.DateField(_('date of end'))
    
    class Meta:
        verbose_name = _('Lot')
        verbose_name_plural = _('Lots')
        ordering = ['-date_of_placement']

    def __str__(self):
        return self.title