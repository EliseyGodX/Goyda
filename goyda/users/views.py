from typing import Any

from core.paginators import CachedPaginator
from core.utils import DataMixin
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.generic import DetailView, FormView, ListView, RedirectView
from users.forms import (LoginUserForm, UserRegistrationForm,
                         UsersPasswordChangeForm)
from users.models import User


@method_decorator(csrf_protect, name='dispatch')
class UsersLoginView(DataMixin, FormView):
    template_name = 'users/login.html'
    form_class = LoginUserForm
    success_url = reverse_lazy('general')
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context_mixin = self.get_default_context(title='Login')
        context.update(context_mixin)
        return context

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)


class UsersLogoutView(RedirectView):
    url = reverse_lazy('general')

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(self.url)


@method_decorator(csrf_protect, name='dispatch')
class UsersRegistrationView(DataMixin, FormView):
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('general')

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context_mixin = self.get_default_context(title='Registration')
        context.update(context_mixin)
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('general')
    
    
class UsersListView(DataMixin, ListView):
    queryset = User.objects.values('username', 'first_name', 'last_name', 'city').order_by('-date_joined')
    context_object_name = 'users'
    template_name = 'users/users.html'
    paginate_by = 10
    paginator_class = CachedPaginator
    cache_key = 'cache_page_{}'
    cache_timeout = 12 * 60
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context_mixin = self.get_default_context(title='Browse')
        context.update(context_mixin)
        return context

    def get_paginator(
        self, queryset, per_page, orphans=0, allow_empty_first_page=True, **kwargs
    ):
        return self.paginator_class(
            queryset,
            per_page,
            orphans=orphans,
            cache_key=self.cache_key,
            cache_timeout=self.cache_timeout,
            allow_empty_first_page=allow_empty_first_page,
            **kwargs,
        )
    
    
    
class UsersPasswordChangeView(LoginRequiredMixin, DataMixin, PasswordChangeView):
    form_class = UsersPasswordChangeForm
    template_name = 'users/change_password.html'
    success_url = reverse_lazy('general')
    login_url = 'users:login'

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context_mixin = self.get_default_context(title='Change password')
        context.update(context_mixin)
        return context
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["new_password1"]) 
        if commit:
            user.save()
            
            
class UsersTrackPurchasesView(LoginRequiredMixin, DataMixin, DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'users/track_purchases.html'
    login_url = 'users:login'
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context_mixin = self.get_default_context(title='Track purchases')
        context.update(context_mixin)
        return context
    
    def get_object(self, queryset=None):
        return self.request.user 
    
    
class UsersTrackSalesView(LoginRequiredMixin, DataMixin, DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'users/track_sales.html'
    login_url = 'users:login'
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context_mixin = self.get_default_context(title='Track sales')
        context.update(context_mixin)
        return context
    
    def get_object(self, queryset=None):
        return self.request.user 