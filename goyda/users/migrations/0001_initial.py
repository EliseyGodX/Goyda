# Generated by Django 5.0.2 on 2024-04-24 10:22

import core.validators
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import django_ulid.models
import ulid.api.api
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', django_ulid.models.ULIDField(default=ulid.api.api.Api.new, editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=48, validators=[core.validators.NameValidator(only_letters=True)], verbose_name='First name')),
                ('last_name', models.CharField(max_length=48, validators=[core.validators.NameValidator(only_letters=True)], verbose_name='Last name')),
                ('email', models.EmailField(max_length=254, verbose_name='Email address')),
                ('avatar', models.ImageField(default='avatars/default.jpg', upload_to='avatars', verbose_name='Avatar')),
                ('age', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(100)], verbose_name='Age')),
                ('balance', models.PositiveBigIntegerField(default=0, verbose_name='Balance')),
                ('about', models.TextField(blank=True, null=True, verbose_name='About')),
                ('phone', models.CharField(blank=True, max_length=28, null=True, validators=[core.validators.PhoneNumberValidator()], verbose_name='Phone number')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_cities', to='core.city', verbose_name='City')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'db_table_comment': 'Contains information about the user"',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
