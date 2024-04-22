from categories.models import Category
from django.core.cache import cache
from users.models import User


class DataMixin:
    
    def get_default_context(self, **kwargs):
        context = kwargs
        
        if 'title' not in context: 
            context['title'] = 'Goyda'
            
        categories = cache.get('categories')
        if not categories:
            categories = list(Category.objects.all().values('name', 'slug'))
            cache.set('categories', categories, timeout=60*60)
        context['categories'] = categories
        
        context['active_purchases'] = User.objects.filter(pk=self.request.user.pk).exclude(active_purchases=None).count()
        context['active_sell'] = User.objects.filter(pk=self.request.user.pk).exclude(active_sell=None).count()
        
        return context