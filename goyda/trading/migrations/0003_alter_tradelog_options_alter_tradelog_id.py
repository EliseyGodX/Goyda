# Generated by Django 5.0.2 on 2024-04-24 16:17

import django_ulid.models
import ulid.api.api
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trading', '0002_alter_tradelog_buyer_alter_tradelog_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tradelog',
            options={'ordering': ('-id',), 'verbose_name': 'Trade Log', 'verbose_name_plural': 'Trade Logs'},
        ),
        migrations.AlterField(
            model_name='tradelog',
            name='id',
            field=django_ulid.models.ULIDField(default=ulid.api.api.Api.new, editable=False, primary_key=True, serialize=False),
        ),
    ]