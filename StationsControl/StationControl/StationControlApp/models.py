from django.urls import reverse
from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth.models import User


class Station(models.Model):
    STATES = (('1', 'running'),
              ('2', 'broken'))

    title = models.CharField(max_length=200)
    state = models.CharField(choices=STATES, max_length=8, default=STATES[0][1], editable=False)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", null=True, blank=True)
    time_create = models.DateTimeField(auto_now_add=True, editable=False)
    time_broken = models.DateTimeField(null=True, blank=True, editable=False)

    x_position = models.IntegerField(default=100, editable=False)
    y_position = models.IntegerField(default=100, editable=False)
    z_position = models.IntegerField(default=100, editable=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('stations/', kwargs={'station_id': self.pk})

    class Meta:
        verbose_name_plural = 'Stations'
        verbose_name = 'Station title'


class Indication(models.Model):
    AXIS = (('1', 'x'),
            ('2', 'y'),
            ('3', 'z'))
    user = models.ForeignKey(
        User,
        default=None,
        null=True,
        on_delete=models.CASCADE
    )
    axis = models.CharField(choices=AXIS, max_length=2, default=AXIS[0][1])
    distance = models.IntegerField()
