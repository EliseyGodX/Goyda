from bids.models import Bid
from categories.models import Category
from django.core.cache import cache
from trading.models import TradeLog


class DataMixin:
    
    def get_default_context(self, **kwargs):
        context = kwargs
        user_id = self.request.user.pk
        if 'title' not in context: 
            context['title'] = 'Goyda'
        categories = cache.get('categories')
        if not categories:
            categories = list(Category.objects.values('name', 'slug').all())
            cache.set('categories', categories, timeout=60*60)
        context['categories'] = categories
        
        if user_id:
            purchases = cache.get(f'status_bar.purchases.{user_id}')
            sell = cache.get(f'status_bar.sell.{user_id}')
            if purchases is None or sell is None:
                purchases = Bid.objects.filter(user_id=user_id, trade__status=1).values('trade_id').distinct().count()
                sell = TradeLog.objects.filter(lot_id__seller_id=user_id, status=1).count()
                cache.set(f'status_bar.purchases.{user_id}', purchases, 60)
                cache.set(f'status_bar.sell.{user_id}', sell, 60)
            context['purchases'] = purchases
            context['sell'] = sell
            context['balance'] = self.request.user.balance
            
        return context