from django import forms
from django.utils.translation import gettext_lazy as _
from users.models import User


class AccountsEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 
                  'avatar', 'age', 'email', 'about', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
            # 'city': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control', 'type': 'file'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'type': 'email'}),
            'about': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'type': 'tel'}),
        }