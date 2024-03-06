# Generated by Django 5.0.2 on 2024-03-06 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lots', '0003_category_path_alter_lots_date_of_end_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=48, unique=True, verbose_name='Category name'),
        ),
        migrations.AlterField(
            model_name='category',
            name='path',
            field=models.CharField(max_length=48, unique=True, verbose_name='Path name'),
        ),
    ]
