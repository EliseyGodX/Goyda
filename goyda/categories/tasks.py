from categories.models import Category
from celery import Celery
from core.paginators import PAGINATE_SETTINGS, CachedPaginator
from django.conf import settings
from django.db.models import CharField, F, Value
from django.db.models.functions import Concat

app = Celery()


@app.task
def update_LotsByCategoryView_paginator():
    per_page = PAGINATE_SETTINGS['LotsByCategoryView']['pagination_by']
    cache_key = PAGINATE_SETTINGS['LotsByCategoryView']['cache_key']
    cache_timeout = PAGINATE_SETTINGS['LotsByCategoryView']['cache_timeout']
    categories = Category.objects.only('slug').all()
    for category in categories:
        queryset = (PAGINATE_SETTINGS['LotsByCategoryView']['queryset']
                .filter(lot__category__slug=category.slug, status=1)
                .annotate(
                    lot_title=F('lot__title'),
                    lot_picture_url=Concat(Value(settings.MEDIA_URL), F('lot__picture'), output_field=CharField())
                ))        
        CachedPaginator(object_list=queryset, cache_timeout=cache_timeout, 
                    per_page=per_page, cache_key=cache_key + '_' + category.slug + '_{}').update_cache()