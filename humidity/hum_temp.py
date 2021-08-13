import Adafruit_DHT
import gpiozero
import time
from datetime import datetime, timedelta
from .models import HumidityTemp, HumidityTempValues, Exhaust
from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.triggers.cron import CronTrigger
from schedule.start_schedule import button_relay_job

jobstores = {
  'default': SQLAlchemyJobStore(url='postgresql+psycopg2://pi:rnautomations@db:5432/arc_db')
#   'default': SQLAlchemyJobStore(url='postgresql+psycopg2://pi:rnautomations@localhost:5432/arc_db')
}
executors = {
  'default': ThreadPoolExecutor(10),
  'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
  'coalesce': True,
  'max_instances': 25
}

scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc,daemon=True)

def get_humidity_temperature():
	sensor = Adafruit_DHT.DHT22
	pin =4
	new_humidity = 0.0
	new_temperature = 0.0
	for i in range(2):
		humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
		if humidity is not None and temperature is not None:
			humidity = int(humidity)
			new_humidity = humidity
			fahrenheit = (temperature * 9/5) + 32
			new_temperature = int(fahrenheit)
			break
		else:
			print('Failed to retrieve data from humidity sensor.')
			continue
	print(new_humidity,new_temperature)
	return new_humidity, new_temperature

def humidity_temperature_logs():
	sensor = Adafruit_DHT.DHT22
	pin =4
	while True:
		humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
		if humidity is not None and temperature is not None:
			humidity = int(humidity)
			fahrenheit = (temperature * 9/5) + 32
			ht_log = HumidityTemp()
			ht_log.humidity = humidity
			ht_log.temp = int(fahrenheit)
			ht_log.save()
			break
		else:
			print('Failed to retrieve data from humidity sensor.')
			continue

def check_hum_temp():
	sensor = Adafruit_DHT.DHT22
	pin =4
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	if humidity is not None and temperature is not None:
		humidity = int(humidity)
		fahrenheit = (temperature * 9/5) + 32
		try:
			ht_params = HumidityTempValues.objects.get(pk=1)
		except Exception as e:
			ht_params = HumidityTempValues()
			ht_params.pk=1
			ht_params.humidity_value=humidity
			ht_params.buffer_value=5
			ht_params.temp_value=int(fahrenheit)
			ht_params.save()
		ht_params = HumidityTempValues.objects.get(pk=1)
		humidity_positive = ht_params.humidity_value+ht_params.buffer_value
		humidity_nagitive = ht_params.humidity_value-ht_params.buffer_value
		temp_params = ht_params.temp_value+ht_params.buffer_value
		print(humidity_positive, temp_params)
		button_job_id = f'button_relay_job_id_18'
		if humidity >= humidity_positive:
			try:
				e = Exhaust.objects.get(pk=2)
				if e.automation_status == 'True':
					if e.status == 'True':
						print('Exhuast arlready running so continue')
					else:
						e.job_id=button_job_id
						e.status=True
						e.save()
						button_relay_job('True',18,button_job_id)
				else:
					e.job_id=button_job_id
					e.status=False
					e.save()
					button_relay_job('False',18,button_job_id)
			except Exception as e:
				pass


		elif int(fahrenheit) >= temp_params:
			try:
				e = Exhaust.objects.get(pk=2)
				if e.status == 'True':
					print('Exhuast arlready running so continue')
				else:
					e.job_id=button_job_id
					e.status=True
					e.save()
					button_relay_job('True',18,button_job_id)
			except Exception as e:
				pass

		else:
			try:
				e = Exhaust.objects.get(pk=2)
				e.job_id=button_job_id
				e.status=False
				e.save()
				button_relay_job('False',18,button_job_id)
			except Exception as e:
				pass

		button_17_job_id = f'button_relay_job_id_17'
		if humidity <= humidity_nagitive:
			try:
				e = Exhaust.objects.get(pk=1)
				if e.status == 'True':
					print('Exhuast arlready running so continue')
				else:
					e.job_id=button_17_job_id
					e.status=True
					e.save()
					button_relay_job('True',17,button_17_job_id)
			except Exception as e:
				pass

		else:
			try:
				e = Exhaust.objects.get(pk=1)
				e.job_id=button_17_job_id
				e.status=False
				e.save()
				button_relay_job('False',17,button_17_job_id)
			except Exception as e:
				pass

	else:
		print('Failed to retrieve data from humidity sensor.')

def start():
	triggers = CronTrigger(second=5)
	triggers_log = CronTrigger(minute=15)
	scheduler.add_job(check_hum_temp, triggers, id='humidity_temp_job_id', replace_existing=True)
	scheduler.add_job(humidity_temperature_logs, triggers_log, id='humidity_temperature_logs_job_id', replace_existing=True)
	scheduler.start()