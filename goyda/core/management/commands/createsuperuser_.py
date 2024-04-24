from core.models import City
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    help = 'Create a superuser'

    def handle(self, *args, **options):
        User = get_user_model()
        username = input('Username: ')
        password = input('Password: ')
          
        user_data = {
            'username': username,
            'password': password,
            'is_superuser': True,
            'is_staff': True,
            'date_joined': timezone.now(),
            'first_name': 'God',
            'last_name': 'XX',
            'email': 'email.email@email.email',
            'age': 54,
            'city': City.objects.get(name='Чернянка')
        }

        User.objects.create_superuser(**user_data)
        self.stdout.write(self.style.SUCCESS('Successfully'))