from core.utils import DataMixin
from django.core.cache import cache
from django.views.generic import ListView
from lots.models import Lots


class General(DataMixin, ListView):
    context_object_name = 'lots'
    template_name = 'core/general.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_mixin = self.get_default_context()
        context.update(context_mixin)
        return context
    
    def get_queryset(self):
        lots = cache.get('lots')
        if not lots:
            lots = list(Lots.objects.all().defer('title', 'picture', 'current_price'))
            cache.set('lots', lots, timeout=60*2)
        return lots