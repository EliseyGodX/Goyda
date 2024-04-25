from core.validators import NameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_ulid.models import ULIDField, default


class Lot(models.Model):
    
    id = ULIDField(default=default, primary_key=True, editable=False)
    title = models.CharField(_('Title'), max_length=24, validators=[NameValidator()], db_index=True)
    seller = models.ForeignKey('users.User', on_delete=models.PROTECT, db_index=True,
                               related_name='sellers', verbose_name=_('Seller'))
    start_price = models.PositiveBigIntegerField(_('Start price'))
    picture = models.ImageField(_('Picture'), upload_to='lots_imgs', default='default/default_lot.jpg')
    category = models.ForeignKey('categories.Category', on_delete=models.PROTECT, db_index=True,
                                 related_name='categories', verbose_name=_('Lot category'))
    description = models.TextField(_('Description'), blank=True, null=True)
    city = models.ForeignKey('core.City', on_delete=models.PROTECT, db_index=True, 
                             related_name='lot_cities', verbose_name='City')
    date_of_placement = models.DateTimeField(_('date of placement'), auto_now_add=True)
    date_of_end = models.DateField(_('date of end'))
    
    class Meta:
        verbose_name = _('Lot')
        verbose_name_plural = _('Lots')
        ordering = ('-id',)
        db_table_comment = (
            '''The model contains information about the lot. 
            See its status in "trading.TradeLog", see the bids for it in "bids.Bid"'''
            )
        
    def __str__(self):
        return self.title