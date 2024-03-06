# Generated by Django 5.0.2 on 2024-02-28 17:57

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=48, unique=True, verbose_name='category name')),
                ('description', models.TextField(default=None, null=True, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('ID', models.UUIDField(db_index=True, default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=48, verbose_name='Username')),
                ('surname', models.CharField(max_length=48, verbose_name='User surname')),
                ('city', models.CharField(max_length=48, verbose_name="The user's city")),
                ('age', models.PositiveSmallIntegerField(verbose_name="User's age")),
                ('purchases', models.PositiveSmallIntegerField(verbose_name='Purchases made by the user')),
                ('sales', models.PositiveSmallIntegerField(verbose_name='Sales made by the user')),
                ('date_of_registration', models.DateTimeField(auto_now_add=True, verbose_name='Date of user registration')),
                ('balance', models.IntegerField(verbose_name="User's balance")),
                ('about', models.TextField(default=None, null=True, verbose_name='About the user')),
                ('avatar', models.ImageField(upload_to='goyda\\lots\\templates\\lots\\avatars')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name="User's email address")),
                ('phone', models.PositiveSmallIntegerField(unique=True, verbose_name="The user's phone number")),
                ('banned', models.BooleanField(default=False, verbose_name='The user is banned')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'ordering': ['surname'],
            },
        ),
        migrations.CreateModel(
            name='Lots',
            fields=[
                ('ID', models.UUIDField(db_index=True, default=uuid.uuid4, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=48, verbose_name='Lot name')),
                ('picture', models.ImageField(upload_to='goyda\\lots\\templates\\lots\\img_lots')),
                ('cost', models.PositiveIntegerField(verbose_name='The cost of the lot')),
                ('description', models.TextField(verbose_name='Description of the lot')),
                ('city', models.CharField(max_length=48, verbose_name='Sellers City')),
                ('date_of_placement', models.DateTimeField(auto_now_add=True, verbose_name='Date of placement')),
                ('date_of_end', models.DateField(verbose_name='Date of placement')),
                ('category', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='lots.category', verbose_name='lot category')),
                ('buyer', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='buyer', to='lots.users', verbose_name='Buyer')),
                ('seller', models.ForeignKey(on_delete=models.SET(None), related_name='seller', to='lots.users', verbose_name='Seller')),
            ],
            options={
                'verbose_name': 'Lot',
                'verbose_name_plural': 'Lots',
                'get_latest_by': 'date_of_placement',
            },
        ),
    ]