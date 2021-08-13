from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger
from pytz import utc
import gpiozero
from django.db import connection
from datetime import datetime, timedelta, time, date
from .models import Schedule, ScheduleLog, RelayStatus
from humidity.models import Exhaust
from .forms import ScheduleForm, RelayStatusForm
import time
import json
import threading
from django.utils import timezone


jobstores = {
	'default': SQLAlchemyJobStore(url='postgresql+psycopg2://pi:rnautomations@db:5432/arc_db')
# 'default': SQLAlchemyJobStore(url='postgresql+psycopg2://pi:rnautomations@localhost:5432/arc_db')
}
executors = {
	'default': ThreadPoolExecutor(10),
	'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
	'coalesce': True,
	'max_instances': 25
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
	while not break_loop:
		try:
			relay = gpiozero.OutputDevice(int(gpio_pin), active_high=False, initial_value=False)
			print('schedule_relay_job relay on')
			relay.on()
		except Exception as e:
			pass
		relay_status = RelayStatus.objects.get(gpio_pin=gpio_pin)
		if relay_status.schedule_status == 'False':
			break_loop=True
		if end_dt < datetime.now():
			break_loop = True
		time.sleep(1)

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
		relay = gpiozero.OutputDevice(14, active_high=False, initial_value=False)
		while True:
			relay_status = RelayStatus.objects.get(pk=1)
			if relay_status.button_status == 'True' and relay_status.schedule_status == 'False':
				try:
					print(' button_relay_14 relay ON')
					relay.on()
				except Exception as e:
					print(e)
					pass
			elif relay_status.button_status == 'True' and relay_status.schedule_status == 'True':
				break
			else:
				# relay.off()
				break
			time.sleep(1)
	except Exception as e:
		print(e)
		pass

def relay_15():
	try:
		relay = gpiozero.OutputDevice(15, active_high=False, initial_value=False)
		while True:
			relay_status = RelayStatus.objects.get(pk=2)
			if relay_status.button_status == 'True' and relay_status.schedule_status == 'False':
				try:
					print(' button_relay_15 relay ON')
					relay.on()
				except Exception as e:
					print(e)
					pass
			elif relay_status.button_status == 'True' and relay_status.schedule_status == 'True':
				break
			else:
				# relay.off()
				break
			time.sleep(3)
	except Exception as e:
		print(e)
		pass

def relay_17():
	try:
		relay = gpiozero.OutputDevice(17, active_high=False, initial_value=False)
		while True:
			relay_status = Exhaust.objects.get(pk=1)
			if relay_status.status == 'True':
				try:
					print(' button_relay_17 relay ON')
					relay.on()
				except Exception as e:
					print(e)
					pass
			elif relay_status.automation_status == 'False' and relay_status.status == 'True':
				break
			else:
				# relay.off()
				break
			time.sleep(3)
	except Exception as e:
		print(e)
		pass

def relay_18():
	try:
		relay = gpiozero.OutputDevice(18, active_high=False, initial_value=False)
		while True:
			relay_status = Exhaust.objects.get(pk=2)
			if relay_status.status == 'True':
				try:
					print(' button_relay_18 relay ON')
					relay.on()
				except Exception as e:
					print(e)
					pass
			elif relay_status.automation_status == 'False' and relay_status.status == 'True':
				break
			else:
				# relay.off()
				break
			time.sleep(3)
	except Exception as e:
		print(e)
		pass

def start():
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

def add_schedule(how_often_day, how_often,start_dt,schedule_duration,gpio_pin,schedule_job_id):
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
	trigger_list = []
	for often in how_often:
		trigger_list.append(CronTrigger(hour=often.hour, minute=often.minute))
	triggers = OrTrigger(trigger_list)
	scheduler.add_job(schedule_relay, triggers, args=[schedule_duration,gpio_pin,False], id=schedule_job_id, replace_existing=True)
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