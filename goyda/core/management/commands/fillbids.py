import random

from bids.models import Bid
from django.core.management.base import BaseCommand
from trading.models import TradeLog
from users.models import User


class Command(BaseCommand):
    help = 'Fill bids table with initial data'    

    def handle(self, *args, **options):
        self.trade_log = list(TradeLog.objects.only().all())
        self.users = list(User.objects.only().all())
        self.bids = {}
        for i in self.trade_log:
            if random.randint(1, 100) > 35:
                self.bids[i] = random.randint(1, 10)
            else: 
                i.status = 0
                i.save()
        self.generate()
        self.stdout.write(self.style.SUCCESS('Bids: Successfully'))
        
    def generate(self):
        while self.bids:
            trade = random.choice(list(self.bids))
            user = None
            while user is None or user == trade.lot.seller:
                user = random.choice(self.users)
            bid_data = {
                'bid': trade.current_price + random.randint(1, 10) * 10,
                'trade': trade,
                'user': user                
            }
            try: Bid.objects.create(**bid_data)
            except Exception as e: print(e)        
            trade.current_price = bid_data['bid']
            trade.buyer = bid_data['user']
            trade.status = 1
            trade.save()
            self.bids[trade] -= 1
            if self.bids[trade] == 0:
                trade.status = random.randint(0, 1)
                del self.bids[trade]
        
            
            