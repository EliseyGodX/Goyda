# Generated by Django 5.0.2 on 2024-03-25 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lots', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(blank=True, default=None, verbose_name='Description'),
        ),
    ]
