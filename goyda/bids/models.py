from django.db import models
from uuid_extensions import uuid7
from django.utils.translation import gettext_lazy as _

class Bid(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid7())
    trade = models.ForeignKey('trading.TradeLogs', on_delete=models.PROTECT, db_index=True,
                               related_name='trading', verbose_name=_('Trade ID'), 
                               help_text=_('The relationship with the TradeLogs table, which contains information about the lot and a link to the lot'))
    user = models.ForeignKey('users.User', on_delete=models.PROTECT, db_index=True,
                                related_name='users', verbose_name=_('User ID'),
                                help_text=_('The ID of the user who placed the bet'))
    bid = models.PositiveIntegerField(_('Bid'), help_text=_('The amount that the user has set'))
    
    class Meta:
        verbose_name = _('Bid')
        verbose_name_plural = _('Bids')
        db_table_comment = (
            '''The model contains all the information about the bids of all users for all lots.
            Attention! Adding/removing/moving bets without control entails the failure of the entire system.'''
            )
    
    def __str__(self):
        return f'{self.bid} - {self.id}'
    