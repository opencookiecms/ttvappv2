# Generated by Django 3.0.5 on 2020-04-29 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0002_auto_20200429_0529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cameraset',
            name='camera_main',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
