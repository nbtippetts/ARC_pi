from django import template
register = template.Library()
from ..models import Schedule, ScheduleLog, RelayStatus
from allthelogs.models import SelectLogs
from allthelogs.forms import GetLogsForm
from climate.models import Exhaust
from climate.forms import ExhaustForm
from ..forms import RemoveScheduleForm, RelayStatusForm
from climate.models import ClimateLogs, ClimateValues, Exhaust
from climate.forms import ClimateValuesForm, ExhaustForm
from climate.hum_temp import get_humidity_temperature
from datetime import datetime

@register.inclusion_tag('overview_cards.html')
def overview_cards():
	return
@register.inclusion_tag('current_lighting_schedule.html')
def current_lighting_schedule():
	schedule_param = Schedule.objects.filter(gpio_pin=14)
	return {'schedule_param': schedule_param}

@register.inclusion_tag('current_watering_schedule.html')
def current_watering_schedule():
	schedule_param = Schedule.objects.filter(gpio_pin=15)
	return {'schedule_param': schedule_param}

@register.inclusion_tag('gpio_14_schedule_log.html')
def show_gpio_14_schedule_log():
	latest_schedule = ScheduleLog.objects.filter(gpio_pin=14).order_by('-id')[:5]
	# try:
	# 	get_dates = SelectLogs.objects.get(gpio_pin=14)
	# 	print(get_dates.start_date)
	# 	print(get_dates.end_date)
	# 	latest_schedule = ScheduleLog.objects.filter(gpio_pin=14,
	# 				finish_date__gte=get_dates.start_date,
	# 				finish_date__lte=get_dates.end_date
	# 			)
	# except SelectLogs.DoesNotExist:
	# 	latest_schedule = ScheduleLog.objects.filter(gpio_pin=14).order_by('-id')[:5]
	# 	pass
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
def show_gpio_15_schedule_log():
	latest_schedule = ScheduleLog.objects.filter(gpio_pin=15).order_by('-id')[:5]
	# try:
	# 	get_dates = SelectLogs.objects.get(gpio_pin=15)
	# 	print(get_dates.start_date)
	# 	print(get_dates.end_date)
	# 	latest_schedule = ScheduleLog.objects.filter(gpio_pin=15,
	# 				finish_date__gte=get_dates.start_date,
	# 				finish_date__lte=get_dates.end_date
	# 			)
	# except SelectLogs.DoesNotExist:
	# 	latest_schedule = ScheduleLog.objects.filter(gpio_pin=15).order_by('-id')[:5]
	# 	pass
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
def show_gpio_3_schedule_log():
	latest_schedule = ScheduleLog.objects.filter(gpio_pin=3).order_by('-id')[:5]
	# try:
	# 	get_dates = SelectLogs.objects.get(gpio_pin=3)
	# 	print(get_dates.start_date)
	# 	print(get_dates.end_date)
	# 	latest_schedule = ScheduleLog.objects.filter(gpio_pin=3,
	# 				finish_date__gte=get_dates.start_date,
	# 				finish_date__lte=get_dates.end_date
	# 			)
	# except SelectLogs.DoesNotExist:
	# 	latest_schedule = ScheduleLog.objects.filter(gpio_pin=3).order_by('-id')[:5]
	# 	pass
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

@register.inclusion_tag('remove_schedule.html')
def remove_schedule():
	form = RemoveScheduleForm()
	return {'form': form}

@register.inclusion_tag('relay_14.html')
def gpio_14_state():
	relay_state = RelayStatus.objects.get(pk=1)
	form = RelayStatusForm(initial={
		'status': relay_state.button_status,
	})
	schedule_status = relay_state.schedule_status
	button_status = relay_state.button_status
	pin_state = 0
	if button_status == 'True' or schedule_status == 'True':
		pin_state = 1
	else:
		pin_state = 0
	return {'button_form': form, 'gpio_14_state':pin_state}

@register.inclusion_tag('relay_15.html')
def gpio_15_state():
	relay_state = RelayStatus.objects.get(pk=2)
	form = RelayStatusForm(initial={
		'status': relay_state.button_status,
	})
	schedule_status = relay_state.schedule_status
	button_status = relay_state.button_status
	pin_state = 0
	if button_status == 'True' or schedule_status == 'True':
		pin_state = 1
	else:
		pin_state = 0
	return {'button_form': form, 'gpio_15_state':pin_state}

@register.inclusion_tag('relay_2.html')
def gpio_2_state():
	relay_state = Exhaust.objects.get(pk=1)
	form = ExhaustForm(initial={
		'status': relay_state.status,
	})
	if relay_state.automation_status == 'True':
		auto_pin_state = 1
	else:
		auto_pin_state = 0
	if relay_state.status == 'True':
		pin_state = 1
	else:
		pin_state = 0
	return {'button_form': form,'gpio_2_state':pin_state, 'gpio_2_auto_state':auto_pin_state}

@register.inclusion_tag('relay_3.html')
def gpio_3_state():
	relay_state = Exhaust.objects.get(pk=2)
	form = ExhaustForm(initial={
		'status': relay_state.status,
	})
	if relay_state.automation_status == 'True':
		auto_pin_state = 1
	else:
		auto_pin_state = 0
	if relay_state.status == 'True':
		pin_state = 1
	else:
		pin_state = 0
	return {'button_form': form,'gpio_3_state':pin_state, 'gpio_3_auto_state':auto_pin_state}

@register.inclusion_tag('gpio_14.html')
def gpio_14_state_function():
	relay_state = RelayStatus.objects.get(pk=1)
	schedule_status = relay_state.schedule_status
	button_status = relay_state.button_status
	pin_state = 0
	if button_status == 'True' or schedule_status == 'True':
		pin_state = 1
	else:
		pin_state = 0
	return {'gpio_14_state':pin_state}

@register.inclusion_tag('gpio_15.html')
def gpio_15_state_function():
	relay_state = RelayStatus.objects.get(pk=2)
	schedule_status = relay_state.schedule_status
	button_status = relay_state.button_status
	pin_state = 0
	if button_status == 'True' or schedule_status == 'True':
		pin_state = 1
	else:
		pin_state = 0
	return {'gpio_15_state':pin_state}

@register.inclusion_tag('gpio_2.html')
def gpio_2_state_function():
	relay_state = Exhaust.objects.get(pk=1)
	pin_state = 0
	auto_pin_state = 0
	if relay_state.status == 'True':
		pin_state = 1
	else:
		pin_state = 0
	if relay_state.automation_status == 'True':
		auto_pin_state = 1
	else:
		auto_pin_state = 0
	return {'gpio_2_state':pin_state,'gpio_2_auto_state':auto_pin_state}

@register.inclusion_tag('gpio_3.html')
def gpio_3_state_function():
	relay_state = Exhaust.objects.get(pk=2)
	pin_state = 0
	auto_pin_state = 0
	if relay_state.status == 'True':
		pin_state = 1
	else:
		pin_state = 0
	if relay_state.automation_status == 'True':
		auto_pin_state = 1
	else:
		auto_pin_state = 0
	return {'gpio_3_state':pin_state,'gpio_3_auto_state':auto_pin_state}


@register.inclusion_tag('current_humidity.html')
def show_humidity():
	current_humidity, current_temp = get_humidity_temperature()
	try:
		check_current_values = ClimateValues.objects.get(pk=2)
	except Exception as e:
		h = ClimateValues(
			pk=2,
			humidity_value=current_humidity,
			temp_value=current_temp,
			start_time=datetime.now().time(),
			end_time=datetime.now().time(),
		)
		h.save()
		check_current_values = ClimateValues.objects.get(pk=2)
		pass
	timenow = datetime.now().time()
	if timenow > check_current_values.start_time and timenow < check_current_values.end_time:
		current_values = ClimateValues.objects.get(pk=2)
	else:
		try:
			current_values = ClimateValues.objects.get(pk=1)
		except Exception as e:
			h = ClimateValues(
				pk=1,
				humidity_value=current_humidity,
				temp_value=current_temp,
				start_time=datetime.now().time(),
				end_time=datetime.now().time(),
			)
			h.save()
			current_values = ClimateValues.objects.get(pk=1)
			pass

	return {'humidity': current_humidity,'temp': current_temp, 'humidity_value':current_values.humidity_value,'temp_value':current_values.temp_value,}

@register.inclusion_tag('current_temp.html')
def show_temp():
	current_temp = show_humidity()
	return {'temp': current_temp['temp'],'temp_value':current_temp['temp_value']}

# @register.inclusion_tag('climate_log_form.html')
# def select_climate_logs():
# 	form = GetLogsForm()
# 	return {'daterange_form': form}
@register.inclusion_tag('log_data.html')
def log_data():
	log_data = ClimateLogs.objects.all().order_by('-id')[:10]
	# try:
	# 	get_dates = SelectLogs.objects.get(gpio_pin=4)
	# 	print(get_dates.start_date)
	# 	print(get_dates.end_date)
	# 	log_data = ClimateLogs.objects.filter(
	# 				created_at__gte=get_dates.start_date,
	# 				created_at__lte=get_dates.end_date
	# 			)
	# except SelectLogs.DoesNotExist:
	# 	log_data = ClimateLogs.objects.all().order_by('-id')[:5]
	# 	pass
	if log_data.exists():
		return {'table_log_data': log_data,}
	else:
		no_data = {
			'start': '00:00:00',
			'duration': '00:00:00',
			'finish_date': '00:00:00'
		}
		return {'table_log_data': no_data}

@register.inclusion_tag('set_climate.html')
def set_climate_form():
	return climate_tag()
@register.inclusion_tag('line_chart.html')
def climate_tag():
	# current_humidity, current_temp = get_humidity_temperature()
	form = ClimateValuesForm()
	log_data = ClimateLogs.objects.all().order_by('-created_at')[:50]
	# try:
	# 	get_dates = SelectLogs.objects.get(gpio_pin=4)
	# 	print(get_dates.start_date)
	# 	print(get_dates.end_date)
	# 	log_data = ClimateLogs.objects.filter(
	# 				created_at__gte=get_dates.start_date,
	# 				created_at__lte=get_dates.end_date
	# 			)
	# except SelectLogs.DoesNotExist:
	# 	log_data = ClimateLogs.objects.all().order_by('-created_at')[:50]
	# 	pass
	try:
		current_values = ClimateValues.objects.get(pk=1)
	except Exception as e:
		h = ClimateValues(
			humidity_value=0.0,
			temp_value=0.0
		)
		h.save()
		pass
	current_values = ClimateValues.objects.get(pk=1)
	return {
		'data': log_data,
		'form':form,
		'humidity_value':current_values.humidity_value,
		'temp_value':current_values.temp_value,}

# @register.inclusion_tag('current_hum_temp.html')
# def current_hum_temp():
# 	current_humidity, current_temp = get_humidity_temperature()
# 	return {
# 		'humidity_value':current_humidity,
# 		'temp_value':current_temp,}
