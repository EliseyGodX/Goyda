from typing import Any

from bids.models import Bid
from core.paginators import PAGINATE_SETTINGS, CachedPaginator
from core.utils import DataMixin
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.views.generic import FormView, ListView, RedirectView
from trading.models import TradeLog
from users.forms import (LoginUserForm, UserRegistrationForm,
                         UsersPasswordChangeForm)


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
    context_object_name = 'users'
    template_name = 'users/users.html'
    queryset = PAGINATE_SETTINGS['UsersListView']['queryset']
    paginate_by = PAGINATE_SETTINGS['UsersListView']['pagination_by']
    cache_key = PAGINATE_SETTINGS['UsersListView']['cache_key']
    cache_timeout = PAGINATE_SETTINGS['UsersListView']['cache_timeout']
    paginator_class = CachedPaginator
    
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
            
            
class UsersTrackPurchasesView(LoginRequiredMixin, DataMixin, View):
    template_name = 'users/track_purchases.html'
    login_url = 'users:login'    
    
    def get_context_data(self, **kwargs: Any):
        context = self.get_default_context(title='Track purchases')        
        active_bids = Bid.objects.filter(
            user_id=self.request.user.id, trade__status=1).select_related('trade', 'trade__lot').all()
        highest_bid = []
        trades = {}
        for bid in active_bids:
            if bid.bid == bid.trade.current_price:
                highest_bid.append(bid.trade)
            if bid.trade.id not in trades: 
                trades[bid.trade.id] = bid.trade
        context['active_trades'] = list(trades.values())
        context['highest_bid'] = highest_bid
        context['completed_trades'] = TradeLog.objects.filter(buyer_id=self.request.user.id).select_related('lot').all()

        return context
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data(**kwargs))
    
    
class UsersTrackSalesView(LoginRequiredMixin, DataMixin, View):
    context_object_name = 'user'
    template_name = 'users/track_sales.html'
    login_url = 'users:login'
    
    def get_context_data(self, **kwargs: Any):
        context = self.get_default_context(title='Track sales')
        queryset = TradeLog.objects.filter(lot__seller_id=self.request.user.id).select_related('lot')
        context['active'] = queryset.filter(status=1).all()
        context['completed'] = queryset.filter(status=0).all()
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data(**kwargs))