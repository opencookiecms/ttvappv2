# Generated by Django 3.0.5 on 2020-05-02 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0003_auto_20200429_0531'),
    ]

    operations = [
        migrations.AddField(
            model_name='cameraset',
            name='test',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
