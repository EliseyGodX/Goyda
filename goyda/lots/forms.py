from core.widgets import CategoryWidget, CityWidget
from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from lots.models import Lot


class LotAddForm(ModelForm):
    date_of_end = forms.DateField(label=_('Date od End'), widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'text'}))
    
    class Meta:
         model = Lot
         fields = ('title', 'start_price', 'picture', 
                   'category', 'description', 'city')
         widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
            'start_price': forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}),
            'picture': forms.FileInput(attrs={'class': 'form-control', 'type': 'file'}),
            'category': CategoryWidget,
            'city': CityWidget
        }
         
         
class LotBidForm(forms.Form):
    bid = forms.IntegerField(label=_('Bid'), widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}))
    
    def __init__(self, *args, **kwargs):
        current_price = kwargs.pop('current_price', None)
        super().__init__(*args, **kwargs)
        if current_price is not None:
            self.fields['bid'].widget.attrs['placeholder'] = f'Current price: {current_price}'

         