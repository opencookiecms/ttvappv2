# Generated by Django 3.0.5 on 2020-06-24 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0011_auto_20200624_0642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryproduct',
            name='product_febexcrate',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='inventoryproduct',
            name='product_totalprice',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5),
        ),
    ]
