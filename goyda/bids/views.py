import math
from typing import Any

from bids.forms import BidForm
from bids.models import Bid
from core.utils import DataMixin
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import CharField, F, Value
from django.db.models.functions import Concat
from django.http import Http404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView
from trading.models import TradeLog


class BidView(LoginRequiredMixin, DataMixin, FormView):
    template_name = 'bids/bid.html'
    form_class = BidForm
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
        bid = form.save(commit=False)
        user = self.request.user
        step = math.ceil(self.lot['lot__start_price'] * 0.1)
        if user.balance < bid.bid:
            form.add_error('bid', _("insufficient funds"))
        if bid.bid - self.lot['current_price'] < step:
            form.add_error('bid', _("the bid must be 10 procent higher than the starting price") + f" ({step})") 
        if form.errors:
            return self.form_invalid(form)
        
        trade = TradeLog.objects.get(lot_id=self.kwargs['lot_id'])
        if trade.status == 0: raise Http404
        last_buyer = Bid.objects.filter(trade_id=trade.id).first()
        with transaction.atomic():
            if last_buyer is not None:
                if last_buyer.user != user:
                    last_buyer.user.balance += trade.current_price 
                    user.balance -= bid.bid
                else: 
                    user.balance -= (bid.bid - trade.current_price)
                last_buyer.user.save()
            else:
                user.balance -= bid.bid
            trade.current_price = bid.bid
            bid.user = user
            bid.trade = trade
            trade.save()
            user.save()
            bid.save()
        return super().form_valid(form)