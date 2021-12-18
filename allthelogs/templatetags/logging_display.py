from django import template
register = template.Library()
from schedule.models import ScheduleLog
from ..models import SelectLogs
from ..forms import GetLogsForm
from climate.models import ClimateLogs
from datetime import datetime

@register.inclusion_tag('gpio_14_schedule_log.html')
def custom_gpio_14_schedule_log():
	try:
		get_dates = SelectLogs.objects.get(gpio_pin=14)
		print(get_dates.start_date)
		print(get_dates.end_date)
		latest_schedule = ScheduleLog.objects.filter(gpio_pin=14,
					finish_date__gte=get_dates.start_date,
					finish_date__lte=get_dates.end_date
				)
	except SelectLogs.DoesNotExist:
		latest_schedule = ScheduleLog.objects.filter(gpio_pin=14).order_by('-id')[:5]
		pass
	if latest_schedule.exists():
		return {'latest_schedule': latest_schedule}
	else:
		no_data = {
			'start': '00:00:00',
			'duration': '00:00:00',
			'finish_date': '00:00:00'
		}
		return {'latest_schedule': no_data}


@register.inclusion_tag('gpio_15_schedule_log.html')
def custom_gpio_15_schedule_log():
	try:
		get_dates = SelectLogs.objects.get(gpio_pin=15)
		print(get_dates.start_date)
		print(get_dates.end_date)
		latest_schedule = ScheduleLog.objects.filter(gpio_pin=15,
					finish_date__gte=get_dates.start_date,
					finish_date__lte=get_dates.end_date
				)
	except SelectLogs.DoesNotExist:
		latest_schedule = ScheduleLog.objects.filter(gpio_pin=15).order_by('-id')[:5]
		pass
	if latest_schedule.exists():
		return {'latest_schedule': latest_schedule}
	else:
		no_data = {
			'start': '00:00:00',
			'duration': '00:00:00',
			'finish_date': '00:00:00'
		}
		return{'latest_schedule': no_data}

@register.inclusion_tag('gpio_3_schedule_log.html')
def custom_gpio_3_schedule_log():
	try:
		get_dates = SelectLogs.objects.get(gpio_pin=23)
		print(get_dates.start_date)
		print(get_dates.end_date)
		latest_schedule = ScheduleLog.objects.filter(gpio_pin=23,
					finish_date__gte=get_dates.start_date,
					finish_date__lte=get_dates.end_date
				)
	except SelectLogs.DoesNotExist:
		latest_schedule = ScheduleLog.objects.filter(gpio_pin=23).order_by('-id')[:5]
		pass
	if latest_schedule.exists():
		return {'latest_schedule': latest_schedule}
	else:
		no_data = {
			'start': '00:00:00',
			'duration': '00:00:00',
			'finish_date': '00:00:00'
		}
		return{'latest_schedule': no_data}


@register.inclusion_tag('log_form.html')
def select_logs():
	form = GetLogsForm()
	return {'daterange_form': form}


@register.inclusion_tag('log_data.html')
def log_data():
	try:
		get_dates = SelectLogs.objects.get(gpio_pin=4)
		print(get_dates.start_date)
		print(get_dates.end_date)
		log_data = ClimateLogs.objects.filter(
					created_at__gte=get_dates.start_date,
					created_at__lte=get_dates.end_date
				)
	except SelectLogs.DoesNotExist:
		log_data = ClimateLogs.objects.all().order_by('-id')[:5]
		pass
	if log_data.exists():
		return {'table_log_data': log_data,}
	else:
		no_data = {
			'start': '00:00:00',
			'duration': '00:00:00',
			'finish_date': '00:00:00'
		}
		return {'table_log_data': no_data}
