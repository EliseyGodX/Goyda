from typing import Any

from core.utils import DataMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView
from users.accounts.forms import AccountsEditForm
from users.models import User


class AccountsPersonalView(LoginRequiredMixin, DataMixin, DetailView):
    model = User
    context_object_name = 'user' 
    template_name = 'accounts/personal.html'
    login_url = 'users:login'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context_mixin = self.get_default_context(title='Personal account')
        context.update(context_mixin)
        return context
    
    def get_object(self, queryset=None):
        return self.request.user 
    
    
class AccountsEditView(LoginRequiredMixin, DataMixin, UpdateView):
    model = User
    context_object_name = 'user' 
    template_name = 'accounts/edit.html'
    form_class = AccountsEditForm
    success_url = reverse_lazy('users:accounts:personal')
    login_url = 'users:login'
        
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context_mixin = self.get_default_context(title='Edit accounts')
        context.update(context_mixin)
        return context
    
    def get_object(self, queryset=None):
        return self.request.user 
    

class AccountsBrowseView(DataMixin, DetailView):
    model = User
    slug_url_kwarg = 'username'
    slug_field = "username"
    context_object_name = 'user' 
    template_name = 'accounts/browse.html'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context_mixin = self.get_default_context(title='Account')
        context.update(context_mixin)
        return context