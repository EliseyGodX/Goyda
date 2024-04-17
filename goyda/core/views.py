from core.utils import DataMixin
from django.views.generic import ListView
from lots.models import Lots
from users.models import User


class General(DataMixin, ListView):
    context_object_name = 'lots'
    template_name = 'core/general.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_mixin = self.get_default_context()
        context.update(context_mixin)
        return context
    
    def get_queryset(self):
        return Lots.objects.only('title', 'picture', 'current_price')