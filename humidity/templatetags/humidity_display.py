from django import template
register = template.Library()
from ..models import HumidityTemp, HumidityTempValues, Exhaust
from ..forms import HumidityTempForm, ExhaustForm
from ..hum_temp import get_humidity_temperature
from schedule.models import RelayStatus, Schedule
from schedule.forms import RelayStatusForm

@register.inclusion_tag('current_humidity.html')
def show_humidity():
	current_humidity, current_temp = get_humidity_temperature()
	try:
		current_values = HumidityTempValues.objects.get(pk=1)
	except Exception as e:
		h = HumidityTempValues(
			humidity_value=current_humidity,
			temp_value=current_temp
		)
		h.save()
		current_values = HumidityTempValues.objects.get(pk=1)
		pass
	return {'humidity': current_humidity,'temp': current_temp, 'humidity_value':current_values.humidity_value,'temp_value':current_values.temp_value,}

@register.inclusion_tag('current_temp.html')
def show_temp():
	current_temp = show_humidity()
	return {'temp': current_temp['temp'],'temp_value':current_temp['temp_value']}

@register.inclusion_tag('line_chart.html')
def humidity_tag():
	# current_humidity, current_temp = get_humidity_temperature()
	form = HumidityTempForm()
	data = HumidityTemp.objects.all().order_by('-created_at')[:100]
	try:
		current_values = HumidityTempValues.objects.get(pk=1)
	except Exception as e:
		h = HumidityTempValues(
			humidity_value=0.0,
			temp_value=0.0
		)
		h.save()
		current_values = HumidityTempValues.objects.get(pk=1)
		pass
	return {
		'data': data,
		'form':form,
		'humidity_value':current_values.humidity_value,
		'temp_value':current_values.temp_value,}

@register.inclusion_tag('current_lighting_schedule.html')
def current_lighting_schedule():
	try:
		schedule_param = Schedule.objects.get(gpio_pin=14)
		return {'schedule_param': schedule_param}
	except Exception as e:
		return {'schedule_param': 'None'}
@register.inclusion_tag('current_watering_schedule.html')
def current_watering_schedule():
	try:
		schedule_param = Schedule.objects.get(gpio_pin=15)
		return {'schedule_param': schedule_param}
	except Exception as e:
		return {'schedule_param': 'None'}

@register.inclusion_tag('current_hum_temp.html')
def current_hum_temp():
	try:
		current_values = HumidityTempValues.objects.get(pk=1)
	except Exception as e:
		h = HumidityTempValues(
			humidity_value=0.0,
			temp_value=0.0
		)
		h.save()
		current_values = HumidityTempValues.objects.get(pk=1)
		pass
	return {
		'humidity_value':current_values.humidity_value,
		'buffer_value':current_values.buffer_value,
		'temp_value':current_values.temp_value,}

@register.inclusion_tag('log_data.html')
def log_data():
	log_data = HumidityTemp.objects.all().order_by('-created_at')[:25]
	return {
		'table_log_data': log_data,}

@register.inclusion_tag('set_humidity_temp.html')
def humidity_temp_form():
	return humidity_tag()

@register.inclusion_tag('relay_14.html')
def gpio_14_state():
	relay_state = RelayStatus.objects.get(pk=1)
	form = RelayStatusForm(initial={
		'status': relay_state.button_status,
	})
	return {'button_form': form}

@register.inclusion_tag('relay_15.html')
def gpio_15_state():
	relay_state = RelayStatus.objects.get(pk=2)
	form = RelayStatusForm(initial={
		'status': relay_state.button_status,
	})
	return {'button_form': form}

@register.inclusion_tag('relay_17.html')
def gpio_17_state():
	relay_state = Exhaust.objects.get(pk=1)
	form = ExhaustForm(initial={
		'status': relay_state.status,
	})
	return {'button_form': form}

@register.inclusion_tag('relay_18.html')
def gpio_18_state():
	relay_state = Exhaust.objects.get(pk=2)
	form = ExhaustForm(initial={
		'status': relay_state.status,
	})
	pin_state = 0
	if relay_state.automation_status == 'True':
		auto_pin_state = 1
	else:
		auto_pin_state = 0
	return {'button_form': form, 'gpio_18_auto_state':auto_pin_state}

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

@register.inclusion_tag('gpio_17.html')
def gpio_17_state_function():
	relay_state = Exhaust.objects.get(pk=1)
	pin_state = 0
	if relay_state.status == 'True':
		pin_state = 1
	else:
		pin_state = 0
	return {'gpio_17_state':pin_state}

@register.inclusion_tag('gpio_18.html')
def gpio_18_state_function():
	relay_state = Exhaust.objects.get(pk=2)
	pin_state = 0
	if relay_state.status == 'True':
		pin_state = 1
	else:
		pin_state = 0
	return {'gpio_18_state':pin_state}