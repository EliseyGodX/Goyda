import itertools

from core.utils import DataMixin
from django.core.cache import cache
from django.views.generic import TemplateView
from trading.models import TradeLog


class GeneralView(DataMixin, TemplateView):
    template_name = 'core/general.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_mixin = self.get_default_context()
        general_view = cache.get('general_view')
        if not general_view:
            pages = [0, 4, 8]
            general_view = {}
            for category in context_mixin['categories']:
                lots = TradeLog.objects.only(
                    'lot__title', 'lot__picture', 'current_price').select_related('lot').filter(
                        lot__category__slug=category['slug'], status=1).all()[:12]
                general_view[category['name']] = {}
                for page in pages:
                    sliced_lots = itertools.islice(lots, page, page + 4)
                    general_view[category['name']][f'pages_{page}'] = list(sliced_lots)
            cache.set('general_view', general_view, 60*5)
        context['general_view'] = general_view
        context.update(context_mixin)
        return context 