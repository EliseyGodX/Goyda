from datetime import timedelta
from typing import Any

from core.utils import DataMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.generic import FormView
from lots.forms import AddLotForm
from lots.tasks import lot_lifetime
from trading.models import TradeLog
from dateutil import parser

@method_decorator(csrf_protect, name='dispatch')
class NewLotView(LoginRequiredMixin, DataMixin, FormView):
    template_name = 'lots/lot_form.html'
    form_class = AddLotForm
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
        delay = date_of_end - timezone.now().date()
        lot_lifetime.apply_async(args=[str(trade.id)], countdown=delay.total_seconds(), broker='redis://localhost:6379/0')
        trade.save()
        return super().form_valid(form)