from django.apps import AppConfig

class ScheduleConfig(AppConfig):
	name = 'schedule'

	def ready(self):
		from . import start_schedule
		start_schedule.start()
