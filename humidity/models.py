from django.db import models
from django.utils import timezone


class HumidityTemp(models.Model):
	humidity = models.IntegerField(default=0)
	temp = models.IntegerField(default=0)
	created_at = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.humidity, self.temp

class HumidityTempValues(models.Model):
	humidity_value = models.IntegerField(default=0)
	buffer_value = models.IntegerField(default=0)
	temp_value = models.IntegerField(default=0)
	created_at = models.DateTimeField(default=timezone.now)

class Exhaust(models.Model):
	job_id = models.TextField(default='')
	status = models.TextField(default='')
	automation_status = models.TextField(default='True')
	created_at = models.DateTimeField(default=timezone.now)
