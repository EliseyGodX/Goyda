from typing import Any

from core.utils import DataMixin
from django.views.generic import ListView
from lots.models import Lots


class General(DataMixin, ListView):
    model = Lots
    context_object_name = 'lots'
    template_name = 'core/general.html'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context_mixin = self.get_default_context()
        context.update(context_mixin)
        return context