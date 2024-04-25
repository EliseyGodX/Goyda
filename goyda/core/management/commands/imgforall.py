import os
import random

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from lots.models import Lot
from users.models import User


class Command(BaseCommand):
    help = 'Random img for all lots and users'

    def handle(self, *args, **kwargs):
        default_avatars_dir = os.path.join(settings.MEDIA_ROOT, 'default/')
        avatars = os.listdir(default_avatars_dir)

        for user in User.objects.all():
            avatar_name = random.choice(avatars)
            avatar_path = os.path.join(default_avatars_dir, avatar_name)
            with open(avatar_path, 'rb') as avatar_file:
                profile, created = User.objects.get_or_create(username=user)
                profile.avatar.save(avatar_name, File(avatar_file), save=True)
                
        for lot in Lot.objects.all():
            avatar_name = random.choice(avatars)
            avatar_path = os.path.join(default_avatars_dir, avatar_name)
            with open(avatar_path, 'rb') as avatar_file:
                profile, created = Lot.objects.get_or_create(id=lot.id)
                profile.picture.save(avatar_name, File(avatar_file), save=True)