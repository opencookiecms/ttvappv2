# Generated by Django 3.0.5 on 2020-05-22 05:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0007_auto_20200522_0355'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventoryproduct',
            name='product_duration',
        ),
    ]
