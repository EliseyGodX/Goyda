from datetime import timedelta
from typing import Any

from core.utils import DataMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.generic import DetailView, FormView
from lots.forms import LotAddForm
from lots.models import Lot
from lots.tasks import lot_lifetime
from trading.models import TradeLog


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
    

