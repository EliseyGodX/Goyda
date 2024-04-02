from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from category.models import Category
from lots.models import Lots


class LotsByCategory(ListView):
    model = Lots
    context_object_name = 'lots'
    template_name = 'category/category.html'
    
    def get_queryset(self) -> QuerySet[Any]:
        return Lots.objects.filter(category__slug=self.kwargs['category_slug'])
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(slug=self.kwargs['category_slug'])
        context['title'] = category.name
        context['categories'] = Category.objects.all()
        context['description'] = category.description
        return context