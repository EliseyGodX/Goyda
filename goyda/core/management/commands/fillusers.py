import random

from core.models import City
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker



class Command(BaseCommand):
    help = 'Fill users table with initial data'    

    def handle(self, *args, **options):
        self.User = get_user_model()
        self.fake = Faker()
        if not args:
            count = int(input('Required number of users:'))
        else: count = args[0]
        self.cities = City.objects.only().all()
        duplicat = self.generate(count)
        while duplicat != 0:
            duplicat = self.generate(duplicat)
        self.stdout.write(self.style.SUCCESS('Users: Successfully'))
        
    def generate(self, count: int):
        duplicat = 0
        for _ in range(count):
            user_data = {
                'username': self.fake.user_name(),
                'password': make_password('QweQweQwe'),
                'is_superuser': False,
                'is_staff': True,
                'date_joined': timezone.now(),
                'first_name': self.fake.first_name(),
                'last_name': self.fake.last_name(),
                'email': self.fake.email(),
                'age': random.randint(18, 99),
                'city': random.choice(self.cities),
                'balance': random.randint(0, 10000),
                'about': self.fake.text(),
                'phone': f'+{self.fake.phone_number()}'
            }
            try: self.User.objects.create(**user_data)
            except Exception as e: print(e)
            if _ % 100 == 1 and _ != 1: print('Added 100 users')
        return duplicat