import datetime
import random

from categories.models import Category
from core.models import City
from django.core.management.base import BaseCommand
from faker import Faker
from lots.models import Lot
from trading.models import TradeLog
from users.models import User


class Command(BaseCommand):
    help = 'Fill lots and trade table with initial data'    

    def handle(self, *args, **options):
        self.fake = Faker()
        if not args:
            count = int(input('Required number of lots:'))
        else: count = args[0]
        self.cities = City.objects.only().all()
        self.categories = Category.objects.only().all()
        self.users = list(User.objects.only().all())
        self.generate(count)
        self.stdout.write(self.style.SUCCESS('Lots: Successfully'))
        
    def generate(self, count: int):
        for _ in range(count):
            start_date = datetime.date.today()
            end_date = start_date + datetime.timedelta(weeks=2)
            random_date = start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))
            users_ = random.sample(self.users, k=2)
            seller = users_[0]
            buyer = users_[1]
            lot_data = {
                'title': self.fake.user_name(),
                'start_price': random.randint(10, 1000),
                'description': self.fake.text(),
                'date_of_end': random_date + datetime.timedelta(weeks=1),
                'city': random.choice(self.cities),
                'category': random.choice(self.categories),
                'seller': seller
            }
            try: lot = Lot.objects.create(**lot_data)
            except Exception as e: print(e)
            
            if random.randint(1, 100) > 35:
                buyer = None
            trade_data = {
                'current_price': lot.start_price,
                'status': 1,
                'buyer': buyer,
                'lot': lot                
            }
            try: TradeLog.objects.create(**trade_data)
            except Exception as e: print(e)
            if _ % 100 == 1 and _ != 1: print('Added 100 lots')