# Generated by Django 5.0.2 on 2024-04-26 11:01

import django_ulid.models
import ulid.api.api
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bids', '0002_alter_bid_options_alter_bid_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='id',
            field=django_ulid.models.ULIDField(default=ulid.api.api.Api.new, editable=False, primary_key=True, serialize=False),
        ),
    ]
