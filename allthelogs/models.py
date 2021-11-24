from django.db import models
from django.utils import timezone
from datetime import datetime
# Create your models here.
class SelectLogs(models.Model):
	start_date = models.DateTimeField(default=timezone.now)
	end_date = models.DateTimeField(default=timezone.now)
	gpio_pin = models.IntegerField(default=0)