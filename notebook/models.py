from django.db import models
from django.utils import timezone
from datetime import datetime

# Create your models here.
class NoteBooks(models.Model):
	title = models.CharField(max_length=255)
	body = models.TextField()
	publish_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.title, self.body