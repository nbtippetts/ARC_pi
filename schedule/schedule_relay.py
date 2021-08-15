from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger
from pytz import utc
# import gpiozero
from datetime import datetime, time
from .models import Schedule, ScheduleLog, RelayStatus
from climate.models import Exhaust
import time

class ScheduleRelay(object):
	def __init__(self):
		print('relay')
		self.schedule_relay_14 = 'relay_14'
		# self.schedule_relay_14 = gpiozero.OutputDevice(14, active_high=False, initial_value=False)
		# self.schedule_relay_15 = gpiozero.OutputDevice(15, active_high=False, initial_value=False)
		self.stopped = False

	# def schedule_relay(self, *args):
	# 	print('schedule_relay_job 1')
	# 	gpio_pin = args[1]
	# 	dt = datetime.now()
	# 	end_dt = dt + args[0]
	# 	relay_status = RelayStatus.objects.get(gpio_pin=gpio_pin)
	# 	relay_status.schedule_status=True
	# 	relay_status.gpio_pin=gpio_pin
	# 	relay_status.save()
	# 	start_time = datetime.now()
	# 	break_loop = args[2]
	# 	print(relay_status.schedule_status)
	# 	if end_dt < datetime.now():
	# 		break_loop = True
		# while not break_loop:
		# 	try:
		# 		# relay = gpiozero.OutputDevice(int(gpio_pin), active_high=False, initial_value=False)
		# 		print(f'schedule_relay_job relay {gpio_pin}')
		# 		# relay.on()
		# 	except Exception as e:
		# 		pass
		# 	relay_status = RelayStatus.objects.get(gpio_pin=gpio_pin)
		# 	if relay_status.schedule_status == 'False':
		# 		break_loop=True
		# 	time.sleep(1)

		# relay_status = RelayStatus.objects.get(gpio_pin=gpio_pin)
		# relay_status.schedule_status=False
		# relay_status.gpio_pin=gpio_pin
		# relay_status.save()
		# schedule_log = ScheduleLog()
		# convert_to_time=(datetime.min + args[0]).time()
		# schedule_log.duration = str(convert_to_time)
		# schedule_log.start = start_time
		# schedule_log.gpio_pin = gpio_pin
		# schedule_log.save()

	def stop(self):
		self.stopped = True