from typing import Any

from categories.models import Category
from core.paginators import PAGINATE_SETTINGS, CachedPaginator
from core.utils import DataMixin
from django.conf import settings
from django.db.models import CharField, F, Value
from django.db.models.functions import Concat
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from lots.models import Lot


class LotsByCategoryView(DataMixin, ListView):
    model = Lot
    context_object_name = 'trades'
    template_name = 'category/category.html'
    paginate_by = PAGINATE_SETTINGS['LotsByCategoryView']['pagination_by']
    cache_key = PAGINATE_SETTINGS['LotsByCategoryView']['cache_key']
    paginator_class = CachedPaginator
    cache_timeout = 5 * 60
    
    def get_queryset(self) -> QuerySet[Any]:
        return (PAGINATE_SETTINGS['LotsByCategoryView']['queryset']
                .filter(lot__category__slug=self.kwargs['category_slug'])
                .annotate(
                    lot_title=F('lot__title'),
                    lot_picture_url=Concat(Value(settings.MEDIA_URL), F('lot__picture'), output_field=CharField())
                ))
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        context_mixin = self.get_default_context(title=category.name)
        context['description'] = category.description
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