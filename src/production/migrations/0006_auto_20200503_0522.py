# Generated by Django 3.0.5 on 2020-05-03 05:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0005_producttest'),
    ]

    operations = [
        migrations.RenameField(
            model_name='producttest',
            old_name='test_name',
            new_name='test',
        ),
    ]