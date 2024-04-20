import random

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker


class Command(BaseCommand):
    help = 'Fill user table with initial data'    

    def handle(self, *args, **options):
        User = get_user_model()
        fake = Faker()
        cities = []
        
        count = int(input('Required number of users:'))

        for _ in range(50):
            city = fake.city().lower().replace(" ", "-")
            cities.append(city)
        
        for _ in range(count):
            user_data = {
                'username': fake.user_name(),
                'password': make_password('QweQweQwe'),
                'is_superuser': False,
                'is_staff': True,
                'date_joined': timezone.now(),
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'email': fake.email(),
                'age': random.randint(18, 99),
                'city': random.choice(cities),
                'purchases': random.randint(0, 100),
                'sales': random.randint(0, 100),
                'balance': random.randint(0, 10000),
                'about': fake.text(),
                'phone': f'+{fake.phone_number()}'
            }
            try: User.objects.create(**user_data)
            except: print('Duplicat')
            print(f'Count: {_}')
        self.stdout.write(self.style.SUCCESS('Successfully'))