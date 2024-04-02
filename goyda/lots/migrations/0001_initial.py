# Generated by Django 5.0.2 on 2024-03-31 13:32

import core.validators
import django.db.models.deletion
import lots.models
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lots',
            fields=[
                ('ID', models.UUIDField(db_index=True, default=uuid.uuid4, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=24, validators=[core.validators.NameValidator()], verbose_name='lot name')),
                ('picture', models.ImageField(upload_to='lots_imgs', verbose_name='lot picture')),
                ('cost', models.PositiveIntegerField(verbose_name='the cost of the lot')),
                ('description', models.TextField(blank=True, default=None, verbose_name='description of the lot')),
                ('city', models.CharField(max_length=48, validators=[core.validators.CityValidator()], verbose_name='sellers city')),
                ('date_of_placement', models.DateTimeField(auto_now_add=True, verbose_name='date of placement')),
                ('date_of_end', models.DateField(verbose_name='date of end')),
                ('buyer', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='buyer', to=settings.AUTH_USER_MODEL, verbose_name='buyer')),
                ('category', models.ForeignKey(on_delete=models.SET(lots.models.Lots._get_default_category), to='category.category', verbose_name='lot category')),
                ('seller', models.ForeignKey(on_delete=models.SET(None), related_name='seller', to=settings.AUTH_USER_MODEL, verbose_name='seller')),
            ],
            options={
                'verbose_name': 'Lot',
                'verbose_name_plural': 'Lots',
                'get_latest_by': 'date_of_placement',
            },
        ),
    ]
