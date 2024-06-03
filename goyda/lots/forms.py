from core.widgets import CategoryWidget, CityWidget
from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from lots.models import Lot


class AddLotForm(ModelForm):
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
         