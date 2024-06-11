import math
from datetime import timedelta
from typing import Any

from core.utils import DataMixin
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import CharField, F, Value
from django.db.models.functions import Concat
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.generic import DetailView, FormView
from lots.forms import LotAddForm, LotBidForm
from lots.models import Lot
from lots.tasks import lot_lifetime
from trading.models import TradeLog
from users.models import User


@method_decorator(csrf_protect, name='dispatch')
class AddLotView(LoginRequiredMixin, DataMixin, FormView):
    template_name = 'lots/add.html'
    form_class = LotAddForm
    success_url = reverse_lazy('general')
    login_url = 'users:login'
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context_mixin = self.get_default_context(title='New lot')
        context.update(context_mixin)
        return context
    
    def form_valid(self, form):
        lot = form.save(commit=False)
        lot.seller = self.request.user
        
        date_of_end = form.cleaned_data['date_of_end']
        today = timezone.now().date()
        min_date = today + timedelta(days=1)
        max_date = today + timedelta(weeks=2)
        if date_of_end  < min_date or date_of_end  > max_date:
            form.add_error('date_of_end', _("Date of end must be between tomorrow and 2 weeks ahead"))
            if form.errors:
                return self.form_invalid(form)
        lot.save()
        trade = TradeLog.objects.create(lot=lot, status=1, buyer=None, current_price=lot.start_price)
        trade.save()
        delay = date_of_end - timezone.now().date()
        lot_lifetime.apply_async(args=[str(trade.id)], countdown=delay.total_seconds(),)
        return super().form_valid(form)
    
    
class LotInspectView(DataMixin, DetailView):
    template_name = 'lots/inspect.html'
    slug_url_kwarg = 'lot_id'
    slug_field = 'id'
    context_object_name = 'lot'
    queryset = Lot.objects.select_related('category', 'seller').only(
        'title', 'start_price', 'picture', 'city', 'description', 'category__name', 'category__slug','seller__username')
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context_mixin = self.get_default_context(title='inspect')
        context['trade'] = TradeLog.objects.values('status', 'current_price', 'buyer__username').get(lot_id=self.object.id)
        context['address'] = self.object.city.full_address
        context.update(context_mixin)
        return context
    

class LotBidView(LoginRequiredMixin, DataMixin, FormView):
    template_name = 'lots/bid.html'
    form_class = LotBidForm
    login_url = 'users:login'
    
    def get_trade(self):
        try:
            trade = TradeLog.objects.values(
                'lot__title', 'lot__picture', 'current_price', 'lot__start_price', 'status', 'lot__seller').annotate(
                    lot_picture_url=Concat(Value(settings.MEDIA_URL), F('lot__picture'), output_field=CharField())
                ).get(lot_id=self.kwargs['lot_id'])
            if trade['status'] == 0 or self.request.user.id == trade['lot__seller']: 
                raise TradeLog.DoesNotExist            
        except TradeLog.DoesNotExist:
            raise Http404
        return trade
    
    def get_success_url(self) -> str:
        self.success_url = reverse_lazy("lots:inspect", kwargs={'lot_id': self.kwargs['lot_id']})
        return super().get_success_url()
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context_mixin = self.get_default_context(title='Bid')
        context['lot'] = self.lot
        context['lot_id'] = self.kwargs['lot_id']
        context.update(context_mixin)
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.lot = self.get_trade()
        kwargs['current_price'] = self.lot['current_price']
        return kwargs
    
    def form_valid(self, form):
        bid = form.cleaned_data['bid']
        user = self.request.user
        step = math.ceil(self.lot['lot__start_price'] * 0.1)
        if user.balance < bid:
            form.add_error('bid', _("insufficient funds"))
        if bid - self.lot['current_price'] < step:
            form.add_error('bid', _("the bid must be 10 procent higher than the starting price") + f" ({step})") 
        if form.errors:
            return self.form_invalid(form)
        
        trade = TradeLog.objects.get(lot_id=self.kwargs['lot_id'])
        if trade.status == 0: raise Http404
        last_buyer = trade.buyer
        with transaction.atomic():
            if last_buyer is not None:
                last_buyer.balance += trade.current_price 
            trade.current_price = bid
            trade.buyer = user
            user.balance -= bid
            trade.save()
            user.save()
            last_buyer.save()
        return super().form_valid(form)