from django import template
register = template.Library()
from ..models import Schedule, ScheduleLog, RelayStatus
from climate.models import Exhaust
from climate.forms import ExhaustForm
from ..forms import RemoveScheduleForm, RelayStatusForm

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

@register.inclusion_tag('gpio_14_schedule_log.html')
def show_gpio_14_schedule_log():
	latest_schedule = ScheduleLog.objects.filter(gpio_pin=14).order_by('-id')[:10]
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
	latest_schedule = ScheduleLog.objects.filter(gpio_pin=15).order_by('-id')[:10]
	if latest_schedule.exists():
		return {'latest_schedule': latest_schedule}
	else:
		no_data = {
			'start': '00:00:00',
			'duration': '00:00:00',
			'finish_date': '00:00:00'
		}
		return{'latest_schedule': no_data}


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