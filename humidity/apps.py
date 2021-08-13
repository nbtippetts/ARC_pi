from django.apps import AppConfig

class HumidityConfig(AppConfig):
	name = 'humidity'

	def ready(self):
		from . import hum_temp
		hum_temp.start()