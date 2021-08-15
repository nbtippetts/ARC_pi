from django.shortcuts import render, redirect
from datetime import datetime, date
from .models import Schedule, ScheduleLog, RelayStatus
from climate.models import Exhaust
from .forms import ScheduleForm, RemoveScheduleForm, RelayStatusForm
from . import start_schedule
from django.contrib.auth.decorators import login_required

@login_required
def schedule(request):
	start = datetime.now()
	dtwithoutseconds = start.replace(second=0, microsecond=0)
	form = ScheduleForm(initial={
		'start': dtwithoutseconds
	})
	ScheduleLog.objects.filter(duration=None).delete()
	# schedule_obj = Schedule.objects.all().order_by('-finish')[:3]
	context = {
		'form': form
	}
	return render(request, 'schedule.html',context)

@login_required
def update_schedule(request):
	# If this is a POST request then process the Form data
	if request.method == 'POST':
		form = ScheduleForm(request.POST)
		if form.is_valid():
			schedule_duration = form.cleaned_data['duration']
			start_dt = datetime.combine(date.today(),form.cleaned_data['start'])
			end_dt = start_dt + schedule_duration
			print(end_dt)
			# print(form.cleaned_data['how_often'])
			# schedule_interval = form.cleaned_data['how_often']
			# print(schedule_interval.seconds)
			gpio_pin=form.cleaned_data['gpio_pin']
			pk='0'
			if gpio_pin == '14':
				pk='14'
			else:
				pk='15'
			count = 0

			duration_hours = form.cleaned_data['duration_hours']
			duration_minutes = form.cleaned_data['duration_minutes']
			duration_seconds = form.cleaned_data['duration_seconds']
			if duration_hours == '0':
				duration_display = f'For {duration_minutes} Minutes'
			elif duration_minutes == '0':
				duration_display = f'For {duration_hours} Hours'
			elif duration_hours == '0' and duration_minutes == '0':
				duration_display = f'For {duration_seconds} Seconds'
			else:
				duration_display = f'For {duration_hours} Hours {duration_minutes} Minutes'

			how_often_day = form.cleaned_data['how_often_day']
			how_often = form.cleaned_data['how_often']
			how_often_display = form.cleaned_data['how_often_display']

			try:
				set_schedule = Schedule.objects.get(pk=pk)
				set_schedule.duration=duration_display
				set_schedule.schedule_interval=how_often_display
				set_schedule.gpio_pin=gpio_pin
				set_schedule.save()
			except Exception as e:
				set_schedule = Schedule()
				set_schedule.pk=pk
				set_schedule.duration=duration_display
				set_schedule.schedule_interval=how_often_display
				set_schedule.gpio_pin=gpio_pin
				set_schedule.save()

			schedule_job_id = f'update_schedule_job_id_{gpio_pin}'
			start_schedule.add_schedule(how_often_day, how_often,start_dt,schedule_duration,gpio_pin,schedule_job_id)
			context = {
				'form': form
			}
			return redirect('/schedule', context)

	else:
		form = ScheduleForm()

	context = {
		'form': form
	}
	return render(request, 'schedule.html',context)

@login_required
def remove_schedule_view(request):
	if request.method == 'POST':
		form = RemoveScheduleForm(request.POST)
		if form.is_valid():
			gpio_pin=form.cleaned_data['gpio_pin']
			schedule_job_id = f'update_schedule_job_id_{gpio_pin}'
			start_schedule.remove_schedule(schedule_job_id,gpio_pin)
			context = {
				'form': form
			}
			return redirect('/schedule', context)

	else:
		form = RemoveScheduleForm()

	context = {
		'form': form
	}
	return render(request, 'schedule.html',context)

@login_required
def relay_on_off(request):
	if request.method == 'POST':
		form = RelayStatusForm(request.POST)
		if form.is_valid():
			status=request.POST.get('status')
			auto_status=request.POST.get('auto_status')
			gpio_pin=0
			if request.POST.get('14'):
				pk=1
				gpio_pin=14
				relay_status = RelayStatus.objects.get(pk=pk)
				if status == 'False':
					relay_status.schedule_status=status
					relay_status.button_status=status
					relay_status.save()
				else:
					relay_status.button_status=status
					relay_status.save()
			elif request.POST.get('15'):
				pk=2
				gpio_pin=15
				relay_status = RelayStatus.objects.get(pk=pk)
				if status == 'False':
					relay_status.schedule_status=status
					relay_status.button_status=status
					relay_status.save()
				else:
					relay_status.button_status=status
					relay_status.save()
			elif request.POST.get('17'):
				pk=1
				gpio_pin=17
				if auto_status == None:
					relay_status = Exhaust.objects.get(pk=pk)
					relay_status.status=status
					relay_status.save()
				else:
					relay_status = Exhaust.objects.get(pk=pk)
					relay_status.auto_status=auto_status
					relay_status.save()
			elif request.POST.get('18'):
				pk=2
				gpio_pin=18
				if auto_status == None:
					relay_status = Exhaust.objects.get(pk=pk)
					relay_status.status=status
					relay_status.save()
				else:
					relay_status = Exhaust.objects.get(pk=pk)
					relay_status.auto_status=auto_status
					relay_status.save()
			else:
				print('No GPIO Pin in args')

			button_job_id = ''
			if auto_status == "False":
				button_job_id = f'humidity_temp_job_id'
				start_schedule.button_relay_job(auto_status,gpio_pin,button_job_id)
			elif auto_status == "True":
				button_job_id = f'humidity_temp_job_id'
				start_schedule.button_relay_job(auto_status,gpio_pin,button_job_id)
			else:
				button_job_id = f'button_relay_job_id_{gpio_pin}'
				start_schedule.button_relay_job(status,gpio_pin,button_job_id)
			form = ScheduleForm()
			context = {
				'form': form
			}
			# next = request.POST.get('next','/')
			return redirect(request.META.get('HTTP_REFERER'), context)
	else:
		form = ScheduleForm()
	context = {
		'form': form
	}
	return render(request, 'schedule.html',context)