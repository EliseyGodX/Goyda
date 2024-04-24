from django.db import models
from django.utils.translation import gettext_lazy as _
from django_ulid.models import ULIDField, default


class TradeLog(models.Model):
    
    class Status(models.IntegerChoices):
        ACTIVE = 1, "Lot at auction"
        COMPLETED = 0, "The bidding has been completed"

    id = ULIDField(default=default, primary_key=True, editable=False)
    lot = models.OneToOneField('lots.Lot', on_delete=models.PROTECT, db_index=True,
                               related_name='lots', verbose_name=_('Lot ID'), 
                               help_text=_('The ID of the lot'))
    status = models.PositiveSmallIntegerField(choices=Status.choices, default=Status.ACTIVE)
    buyer = models.ForeignKey('users.User', on_delete=models.PROTECT, db_index=True, null=True,
                                related_name='buyer', verbose_name=_('User ID'),
                                help_text=_('The ID of the user who bought this lot'))
    current_price = models.PositiveIntegerField(_('Current price'),  help_text=_('The current price for the lot'))
    
    class Meta:
        verbose_name = _('Trade Log')
        verbose_name_plural = _('Trade Logs')
        ordering = ('-id',)
        db_table_comment = (
            '''Log with records of the lots status.'''
            )
    
    def __str__(self):
        return f'{self.status} - {self.id}'
    