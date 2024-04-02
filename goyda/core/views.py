from typing import Any
from django.views.generic import ListView
from category.models import Category
from lots.models import Lots


class General(ListView):
    model = Lots
    context_object_name = 'lots'
    template_name = 'core/general.html'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Goyda'
        context['categories'] = Category.objects.all()
        
        return context