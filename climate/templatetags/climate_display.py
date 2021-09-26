from django import template
register = template.Library()
from ..models import ClimateLogs, ClimateValues, Exhaust
from ..forms import ClimateValuesForm, ExhaustForm
from ..hum_temp import get_humidity_temperature
from schedule.models import RelayStatus, Schedule
from schedule.forms import RelayStatusForm
from datetime import datetime

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
	timenow = datetime.now().time()
	if timenow > check_current_values.start_time and timenow < check_current_values.end_time:
		current_values = ClimateValues.objects.get(pk=2)
	else:
		current_values = ClimateValues.objects.get(pk=1)

	return {'humidity': current_humidity,'temp': current_temp, 'humidity_value':current_values.humidity_value,'temp_value':current_values.temp_value,}

@register.inclusion_tag('current_temp.html')
def show_temp():
	current_temp = show_humidity()
	return {'temp': current_temp['temp'],'temp_value':current_temp['temp_value']}

@register.inclusion_tag('line_chart.html')
def climate_tag():
	# current_humidity, current_temp = get_humidity_temperature()
	form = ClimateValuesForm()
	data = ClimateLogs.objects.all().order_by('-created_at')[:50]
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
		'data': data,
		'form':form,
		'humidity_value':current_values.humidity_value,
		'temp_value':current_values.temp_value,}

@register.inclusion_tag('current_lighting_schedule.html')
def current_lighting_schedule():
	schedule_param = Schedule.objects.filter(gpio_pin=14)
	return {'schedule_param': schedule_param}
	# try:
	# except Exception as e:
	# 	return {'schedule_param': []}
@register.inclusion_tag('current_watering_schedule.html')
def current_watering_schedule():
	schedule_param = Schedule.objects.filter(gpio_pin=15)
	return {'schedule_param': schedule_param}
	# try:
	# except Exception as e:
	# 	return {'schedule_param': []}

@register.inclusion_tag('current_hum_temp.html')
def current_hum_temp():
	current_humidity, current_temp = get_humidity_temperature()
	return {
		'humidity_value':current_humidity,
		'temp_value':current_temp,}

@register.inclusion_tag('log_data.html')
def log_data():
	log_data = ClimateLogs.objects.all().order_by('-created_at')[:12]
	return {
		'table_log_data': log_data,}

@register.inclusion_tag('set_climate.html')
def set_climate_form():
	return climate_tag()

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

@register.inclusion_tag('relay_17.html')
def gpio_17_state():
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
	return {'button_form': form,'gpio_17_state':pin_state, 'gpio_17_auto_state':auto_pin_state}

@register.inclusion_tag('relay_18.html')
def gpio_18_state():
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
	return {'button_form': form,'gpio_18_state':pin_state, 'gpio_18_auto_state':auto_pin_state}

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

# @register.inclusion_tag('gpio_17.html')
# def gpio_17_state_function():
# 	relay_state = Exhaust.objects.get(pk=1)
# 	pin_state = 0
# 	auto_pin_state = 0
# 	if relay_state.status == 'True':
# 		pin_state = 1
# 	else:
# 		pin_state = 0
# 	if relay_state.automation_status == 'True':
# 		auto_pin_state = 1
# 	else:
# 		auto_pin_state = 0
# 	return {'gpio_17_state':pin_state,'gpio_17_auto_state':auto_pin_state}

# @register.inclusion_tag('gpio_18.html')
# def gpio_18_state_function():
# 	relay_state = Exhaust.objects.get(pk=2)
# 	pin_state = 0
# 	auto_pin_state = 0
# 	if relay_state.status == 'True':
# 		pin_state = 1
# 	else:
# 		pin_state = 0
# 	if relay_state.automation_status == 'True':
# 		auto_pin_state = 1
# 	else:
# 		auto_pin_state = 0
# 	return {'gpio_18_state':pin_state,'gpio_18_auto_state':auto_pin_state}