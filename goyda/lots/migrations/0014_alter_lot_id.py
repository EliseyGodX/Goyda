# Generated by Django 5.0.2 on 2024-04-26 12:17

import django_ulid.models
import ulid.api.api
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lots', '0013_alter_lot_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lot',
            name='id',
            field=django_ulid.models.ULIDField(default=ulid.api.api.Api.new, editable=False, primary_key=True, serialize=False),
        ),
    ]
