from celery import Celery
from core.paginators import CachedPaginator

from core.paginators import PAGINATE_SETTINGS, CachedPaginator

app = Celery()


@app.task
def update_UsersListView_paginator():
    queryset = PAGINATE_SETTINGS['UsersListView']['queryset']
    per_page = PAGINATE_SETTINGS['UsersListView']['pagination_by']
    cache_key = PAGINATE_SETTINGS['UsersListView']['cache_key']
    cache_timeout = PAGINATE_SETTINGS['UsersListView']['cache_key']
    CachedPaginator(object_list=queryset, cache_timeout=cache_timeout,
                    per_page=per_page, cache_key=cache_key).update_cache()