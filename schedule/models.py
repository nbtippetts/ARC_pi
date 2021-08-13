from django.db import models
from django.utils import timezone
from datetime import datetime

class Schedule(models.Model):
	duration=models.TextField(default='')
	schedule_interval = models.TextField(default='')
	gpio_pin = models.IntegerField(default=0)

class ScheduleLog(models.Model):
	start = models.TimeField(blank=True, null=True)
	duration=models.DurationField(default='00:00:00', null=True)
	finish_date = models.DateTimeField(default=timezone.now)
	next_schedule = models.DateTimeField(default=timezone.now)
	start_date = models.DateTimeField(default=timezone.now)
	gpio_pin = models.IntegerField(default=0)

class RelayStatus(models.Model):
	schedule_status = models.TextField(default='False')
	button_status = models.TextField(default='True')
	gpio_pin = models.IntegerField(default=0)
