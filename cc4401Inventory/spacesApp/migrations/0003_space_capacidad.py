# Generated by Django 2.0.5 on 2018-08-18 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spacesApp', '0002_auto_20180808_1714'),
    ]

    operations = [
        migrations.AddField(
            model_name='space',
            name='capacidad',
            field=models.IntegerField(default=100),
            preserve_default=False,
        ),
    ]