from django import forms
from django.contrib.auth.forms import (AuthenticationForm, SetPasswordForm,
                                       UserCreationForm)
from django.utils.translation import gettext_lazy as _
from users.models import User


class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    password2 = forms.CharField(label=_('Repeat password'), widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name',  'username',
                  'city', 'avatar', 'age', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control', 'type': 'file'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'type': 'email'})
        }
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label=_('Username'), widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'text'}))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    
    

class UsersPasswordChangeForm(SetPasswordForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })