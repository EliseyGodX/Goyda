# Generated by Django 5.0.2 on 2024-03-30 19:48

import core.validators
import django.core.validators
import re
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='about',
            field=models.TextField(blank=True, verbose_name='about the user'),
        ),
        migrations.AddField(
            model_name='user',
            name='age',
            field=models.PositiveSmallIntegerField(default=1, verbose_name="user's age"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='avatars/default.jpg', upload_to='avatars', verbose_name="user's avatar"),
        ),
        migrations.AddField(
            model_name='user',
            name='balance',
            field=models.IntegerField(default=0, verbose_name="user's balance"),
        ),
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.CharField(default=1, max_length=48, verbose_name="the user's city"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='purchases',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='purchases made by the user'),
        ),
        migrations.AddField(
            model_name='user',
            name='sales',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='sales made by the user'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=48, validators=[core.validators.NameValidator()], verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=48, validators=[django.core.validators.RegexValidator(re.compile('^[-\\w]+\\Z'), 'Enter a valid “slug” consisting of Unicode letters, numbers, underscores, or hyphens.', 'invalid')], verbose_name='last name'),
        ),
    ]
