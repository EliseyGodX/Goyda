from categories.models import Category
from core.paginators import PAGINATE_SETTINGS, CachedPaginator
from core.utils import DataMixin
from django.conf import settings
from django.core.cache import cache
from django.db.models import CharField, F, Value
from django.db.models.functions import Concat
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from trading.models import TradeLog


class LotsByCategoryView(DataMixin, ListView):
    context_object_name = 'trades'
    template_name = 'categories/category.html'
    paginate_by = PAGINATE_SETTINGS['LotsByCategoryView']['pagination_by']
    cache_key = PAGINATE_SETTINGS['LotsByCategoryView']['cache_key']
    cache_timeout = PAGINATE_SETTINGS['LotsByCategoryView']['cache_timeout']
    paginator_class = CachedPaginator
    
    def get_queryset(self):
        return (PAGINATE_SETTINGS['LotsByCategoryView']['queryset']
                .filter(lot__category__slug=self.kwargs['category_slug'], status=1)
                .annotate(
                    lot_picture_url=Concat(Value(settings.MEDIA_URL), F('lot__picture'), output_field=CharField())
                ))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = cache.get(f"category_{self.kwargs['category_slug']}")
        if category is None:
            category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
            cache.set(f"category_{self.kwargs['category_slug']}", category)
        context_mixin = self.get_default_context(title=category.name)
        context['description'] = category.description
        context['slug'] = category.slug
        context.update(context_mixin)
        return context
    
    def get_paginator(
        self, queryset, per_page, orphans=0, allow_empty_first_page=True, **kwargs
    ):
        return self.paginator_class(
            queryset,
            per_page,
            orphans=orphans,
            cache_key=self.cache_key + '_' + self.kwargs['category_slug'] + '_{}',
            cache_timeout=self.cache_timeout,
            allow_empty_first_page=allow_empty_first_page,
            **kwargs,
        )
        
        
class CategoriesSearchView(DataMixin, ListView):
    context_object_name = 'trades'
    template_name = 'categories/category.html'
    paginate_by = 4
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_mixin = self.get_default_context(title='Search')
        context['q'] = self.request.GET.get('q')
        context.update(context_mixin)
        return context
    
    def get_queryset(self):
        return (TradeLog.objects.values('current_price', 'lot_id', 'lot__title', 'lot__picture')
                .filter(lot__title__icontains=self.request.GET.get('q'), lot__category__slug=self.kwargs['category_slug'], status=1)
                .annotate(
                    lot_picture_url=Concat(Value(settings.MEDIA_URL), F('lot__picture'), output_field=CharField())
                ))