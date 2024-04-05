from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from category.models import Category
from lots.models import Lots
from core.utils import DataMixin


class LotsByCategory(DataMixin, ListView):
    model = Lots
    context_object_name = 'lots'
    template_name = 'category/category.html'
    
    def get_queryset(self) -> QuerySet[Any]:
        return Lots.objects.filter(category__slug=self.kwargs['category_slug'])
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        context_mixin = self.get_default_context(title=category.name)
        context['description'] = category.description
        context.update(context_mixin)
        return context