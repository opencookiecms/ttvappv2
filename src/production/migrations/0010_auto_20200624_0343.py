# Generated by Django 3.0.5 on 2020-06-24 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0009_auto_20200624_0301'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cameraset',
            old_name='camera_link',
            new_name='camera_link1',
        ),
        migrations.AddField(
            model_name='cameraset',
            name='camera_link2',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
