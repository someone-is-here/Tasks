# Generated by Django 4.1.3 on 2022-11-24 14:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StationControlApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='station',
            name='time_broken',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 10, 3, 48, 44, 484207), editable=False),
        ),
        migrations.AlterField(
            model_name='station',
            name='x_position',
            field=models.IntegerField(default=100, editable=False),
        ),
        migrations.AlterField(
            model_name='station',
            name='y_position',
            field=models.IntegerField(default=100, editable=False),
        ),
        migrations.AlterField(
            model_name='station',
            name='z_position',
            field=models.IntegerField(default=100, editable=False),
        ),
    ]
