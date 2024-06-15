from bids.models import Bid
from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _


class BidForm(ModelForm):
    
    class Meta:
         model = Bid
         fields = ('bid',)
         widgets = {
            'bid': forms.TextInput(attrs={'class': 'form-control', 'type': 'number'})
        }
    
    def __init__(self, *args, **kwargs):
        current_price = kwargs.pop('current_price', None)
        super().__init__(*args, **kwargs)
        if current_price is not None:
            self.fields['bid'].widget.attrs['placeholder'] = f'Current price: {current_price}'