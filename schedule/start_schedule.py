from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger
from pytz import utc
# import gpiozero
# import Adafruit_DHT
from datetime import datetime, time
from .models import Schedule, ScheduleLog, RelayStatus
from climate.models import Exhaust, ClimateValues, ClimateLogs
from climate.models import Exhaust
import time


jobstores = {
	'default': SQLAlchemyJobStore(url='postgresql+psycopg2://pi:rnautomations@db:5432/arc_db')
# 'default': SQLAlchemyJobStore(url='postgresql+psycopg2://pi:rnautomations@localhost:5432/arc_db')
}
executors = {
	'default': ThreadPoolExecutor(10),
	'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
	'coalesce': False,
	'max_instances': 10
}
scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc, daemon=True)

def schedule_relay(*args):
	print('schedule_relay_job 1')
	gpio_pin = args[1]
	dt = datetime.now()
	end_dt = dt + args[0]
	relay_status = RelayStatus.objects.get(gpio_pin=gpio_pin)
	relay_status.schedule_status=True
	relay_status.gpio_pin=gpio_pin
	relay_status.save()
	start_time = datetime.now()
	break_loop = args[2]
	print(relay_status.schedule_status)
	# relay = gpiozero.OutputDevice(int(gpio_pin), active_high=True, initial_value=False)
	while not break_loop:
		try:
			print(f'schedule_relay_job relay {gpio_pin}')

		except Exception as e:
			pass
		relay_status = RelayStatus.objects.get(gpio_pin=gpio_pin)
		if relay_status.schedule_status == 'False':
			break_loop=True
		if end_dt < datetime.now():
			break_loop = True
		time.sleep(5)

	relay_status = RelayStatus.objects.get(gpio_pin=gpio_pin)
	relay_status.schedule_status=False
	relay_status.gpio_pin=gpio_pin
	relay_status.save()
	schedule_log = ScheduleLog()
	convert_to_time=(datetime.min + args[0]).time()
	schedule_log.duration = str(convert_to_time)
	schedule_log.start = start_time
	schedule_log.gpio_pin = gpio_pin
	schedule_log.save()

def relay_14():
	try:
		# relay = gpiozero.OutputDevice(14, active_high=True, initial_value=False)
		while True:
		# while relay.active_high:
			relay_status = RelayStatus.objects.get(pk=1)
			if relay_status.button_status == 'True' and relay_status.schedule_status == 'False':
				try:
					print(' button_relay_14 relay ON')

				except Exception as e:
					print(e)
					pass
			elif relay_status.button_status == 'True' and relay_status.schedule_status == 'True':
				break
			else:
				break
			time.sleep(5)
	except Exception as e:
		print(e)
		pass

def relay_15():
	try:
		# relay = gpiozero.OutputDevice(15, active_high=True, initial_value=False)
		# print(relay.active_high)
		while True:
		# while relay.active_high:
			relay_status = RelayStatus.objects.get(pk=2)
			if relay_status.button_status == 'True' and relay_status.schedule_status == 'False':
				try:
					print(' button_relay_15 relay ON')
					# print(relay.active_high)
				except Exception as e:
					print(e)
					pass
			elif relay_status.button_status == 'True' and relay_status.schedule_status == 'True':
				break
			else:
				break
			time.sleep(5)
	except Exception as e:
		print(e)
		pass

def relay_17():
	try:
		# relay = gpiozero.OutputDevice(17, active_high=True, initial_value=False)
		while True:
		# while relay.active_high:
			relay_status = Exhaust.objects.get(pk=1)
			if relay_status.status == 'True':
				try:
					print(' button_relay_17 relay ON')

				except Exception as e:
					print(e)
					pass
			elif relay_status.automation_status == 'False' and relay_status.status == 'True':
				break
			else:
				break
			time.sleep(5)
	except Exception as e:
		print(e)
		pass

def relay_18():
	try:
		# relay = gpiozero.OutputDevice(18, active_high=True, initial_value=False)
		while True:
		# while relay.active_high:
			relay_status = Exhaust.objects.get(pk=2)
			if relay_status.status == 'True':
				try:
					print(' button_relay_18 relay ON')

				except Exception as e:
					print(e)
					pass
			elif relay_status.automation_status == 'False' and relay_status.status == 'True':
				break
			else:
				break
			time.sleep(5)
	except Exception as e:
		print(e)
		pass

def check_climate():
	# sensor = Adafruit_DHT.DHT22
	pin =4
	humidity, temperature = 69.0,69.0
	# humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	if humidity is not None and temperature is not None:
		humidity = int(humidity)
		fahrenheit = (temperature * 9/5) + 32
		try:
			ht_params = ClimateValues.objects.get(pk=1)
		except Exception as e:
			ht_params = ClimateValues()
			ht_params.pk=1
			ht_params.humidity_value=humidity
			ht_params.buffer_value=5
			ht_params.temp_value=int(fahrenheit)
			ht_params.save()
		ht_params = ClimateValues.objects.get(pk=1)
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
		print('Failed to retrieve data from climate sensor.')

def climate_logs():
	# sensor = Adafruit_DHT.DHT22
	pin =4
	while True:
		humidity, temperature = 69.0,69.0
		# humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
		if humidity is not None and temperature is not None:
			humidity = int(humidity)
			fahrenheit = (temperature * 9/5) + 32
			ht_log = ClimateLogs()
			ht_log.humidity = humidity
			ht_log.temp = int(fahrenheit)
			ht_log.save()
			break
		else:
			print('Failed to retrieve data from climate sensor.')
			time.sleep(1)
			continue

def start():
	triggers = CronTrigger(second='*/5')
	triggers_log = CronTrigger(minute='*/15')
	scheduler.add_job(check_climate, triggers, id='climate_job_id', replace_existing=True)
	scheduler.add_job(climate_logs, triggers_log, id='climate_logs_job_id', replace_existing=True)
	scheduler.start()

def button_relay_job(status,gpio_pin,button_job_id):
	if status == 'False':
		try:
			job_list = scheduler.get_jobs()
			for job in job_list:
				if job.id == button_job_id:
					job.pause()
					job.remove()
		except Exception as e:
			pass
	else:
		if gpio_pin == 14:
			scheduler.add_job(relay_14, id=button_job_id, replace_existing=True)
		elif gpio_pin == 15:
			scheduler.add_job(relay_15, id=button_job_id, replace_existing=True)
		if gpio_pin == 17:
			scheduler.add_job(relay_17, id=button_job_id, replace_existing=True)
		elif gpio_pin == 18:
			scheduler.add_job(relay_18, id=button_job_id, replace_existing=True)
		else:
			return
	return

def add_schedule(how_often_day, how_often,schedule_duration,gpio_pin,schedule_job_id):
	try:
		job_list = scheduler.get_jobs()
		for job in job_list:
			if job.id == schedule_job_id:
				job.pause()
				job.remove()
				relay_status = RelayStatus.objects.get(gpio_pin=gpio_pin)
				relay_status.schedule_status=False
				relay_status.gpio_pin=gpio_pin
				relay_status.save()
	except Exception as e:
		pass
	print(how_often)
	triggers = OrTrigger(CronTrigger(day_of_week=how_often_day, hour=how_often.hour, minute=how_often.minute))
	scheduler.add_job(schedule_relay, triggers, args=[schedule_duration,gpio_pin,False], id=schedule_job_id, misfire_grace_time=None, replace_existing=True)
	return

def remove_schedule(schedule_job_id,gpio_pin):
	try:
		job_list = scheduler.get_jobs()
		for job in job_list:
			if job.id == schedule_job_id:
				job.pause()
				relay_status = RelayStatus.objects.get(gpio_pin=gpio_pin)
				relay_status.schedule_status=False
				relay_status.gpio_pin=gpio_pin
				relay_status.save()
				job.remove()
	except Exception as e:
		pass
	delete_schedule = Schedule.objects.get(gpio_pin=gpio_pin)
	delete_schedule.delete()
	return

def schedule_display_inputs(display,gpio_pin):
	for d in display:
		print(d)
		duration_hours = d[1]
		duration_minutes = d[2]
		if duration_hours == '0':
			duration_display = f'For {duration_minutes} Minutes'
		elif duration_minutes == '0':
			duration_display = f'For {duration_hours} Hours'
		else:
			duration_display = f'For {duration_hours} Hours {duration_minutes} Minutes'
		try:
			set_schedule = Schedule.objects.get(gpio_pin=gpio_pin)
			set_schedule.duration=duration_display
			set_schedule.schedule_interval=d[0]
			set_schedule.gpio_pin=gpio_pin
			set_schedule.save()
		except Exception as e:
			set_schedule = Schedule()
			set_schedule.duration=duration_display
			set_schedule.schedule_interval=d[0]
			set_schedule.gpio_pin=gpio_pin
			set_schedule.save()
	return