from typing import Optional

from django.core.cache import cache
from django.core.exceptions import EmptyResultSet
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils.functional import cached_property


class CachedPaginator(Paginator):
    
    def __init__(self, object_list, per_page, cache_key, model, model_fields, orphans=0, allow_empty_first_page=True, cache_timeout=None):
        super().__init__(object_list, per_page, orphans, allow_empty_first_page)
        self.model = model
        self.cache_timeout = 60 * 60
        self.cache_key = cache_key
        self.model_fields = model_fields
        
    @cached_property
    def count(self):
        count = cache.get(self.cache_key.format('count'))
        if count is None:
            count = self.update_cache('count')
        return count
    
    def page(self, number):
        number = self.validate_number_handler(number)
        data = cache.get(self.cache_key.format(number))
        if data is None:
            data = self.update_cache(number)
        return data
    
    def update_cache(self, get: Optional[str] = None):
        data = list(self.model.objects.values(*self.model_fields).all())
        if data is not None:
            cache.set(self.cache_key.format('count'), len(data), self.cache_timeout)
            for page in range(self.num_pages):
                page += 1
                cache.set(self.cache_key.format(page), self.get_page_for_cache(page), self.cache_timeout)
            if get is not None:
                return cache.get(self.cache_key.format(get))
        else:
            assert EmptyResultSet('cache cannot be updated due to an empty queryset')
        
    def get_page_for_cache(self, number):
        number = self.validate_number_handler(number)
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page
        if top + self.orphans >= self.count:
            top = self.count
        return self._get_page(self.object_list[bottom:top], number, self)
    
    def validate_number_handler(self, number):
        try:
            number = self.validate_number(number)
        except PageNotAnInteger:
            number = 1
        except EmptyPage:
            number = self.num_pages
        return number
    
        
            

    
    

