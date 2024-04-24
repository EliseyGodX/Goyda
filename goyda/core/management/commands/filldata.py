from core.management.commands.fillbids import Command as FillBids
from core.management.commands.filllots import Command as FillLots
from core.management.commands.fillusers import Command as FillUsers
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Fill all data for db'    

    def handle(self, *args, **options):
        count = int(input('Number of users: '))
        FillUsers().handle(count)
        FillLots().handle(count * 5)
        FillBids().handle()
        self.stdout.write(self.style.SUCCESS('Data: Successfully'))
        
            
            