# Generated by Django 4.1.3 on 2022-11-24 14:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('state', models.CharField(choices=[('1', 'running'), ('2', 'broken')], default='running', editable=False, max_length=8)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='photos/%Y/%m/%d/')),
                ('time_create', models.DateTimeField(auto_now_add=True)),
                ('time_broken', models.DateTimeField(default=datetime.datetime(2023, 11, 10, 3, 46, 17, 629453), editable=False)),
                ('x_position', models.IntegerField(default=100)),
                ('y_position', models.IntegerField(default=100)),
                ('z_position', models.IntegerField(default=100)),
            ],
            options={
                'verbose_name': 'Station title',
                'verbose_name_plural': 'Stations',
            },
        ),
    ]