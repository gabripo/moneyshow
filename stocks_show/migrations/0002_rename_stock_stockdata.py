# Generated by Django 4.2.9 on 2024-10-07 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stocks_show', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Stock',
            new_name='StockData',
        ),
    ]