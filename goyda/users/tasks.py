from celery import Celery
from core.paginators import CachedPaginator, PAGINATE_SETTINGS
from users.models import User

app = Celery()


@app.task
def update_UsersListView_paginator():
    queryset = User.objects.values('username', 'first_name', 'last_name', 'city__name')
    per_page = PAGINATE_SETTINGS['UsersListView']['pagination_by']
    cache_key = PAGINATE_SETTINGS['UsersListView']['cache_key']
    CachedPaginator(object_list=queryset, per_page=per_page, cache_key = cache_key).update_cache()