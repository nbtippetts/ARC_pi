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
		'form': form,
	}
	return render(request, 'schedule.html',context)

# @login_required
# def select_logs(request):
# 	if request.method == 'POST':
# 		form = GetLogsForm(request.POST)
# 		if form.is_valid():
# 			start_log=form.cleaned_data['start_log']
# 			end_log=form.cleaned_data['end_log']
# 			gpio_pin=form.cleaned_data['gpio_pin_date_range']
# 			try:
# 				date_logs = SelectLogs.objects.get(gpio_pin=int(gpio_pin))
# 				date_logs.start_date=start_log
# 				date_logs.end_date=end_log
# 				date_logs.gpio_pin=gpio_pin
# 				date_logs.save()
# 			except SelectLogs.DoesNotExist:
# 				date_logs=SelectLogs()
# 				date_logs.start_date=start_log
# 				date_logs.end_date=end_log
# 				date_logs.gpio_pin=gpio_pin
# 				date_logs.save()
# 				pass
# 			context = {
# 				'daterange_form':form,
# 			}
# 			return redirect('/schedule', context)
# 	else:
# 		form = GetLogsForm()

# 	context = {
# 		'daterange_form': form
# 	}
# 	return render(request, 'schedule.html',context)
@login_required
def update_schedule(request):
	# If this is a POST request then process the Form data
	if request.method == 'POST':
		if request.POST['gpio_pin']=='18':
			print(request.POST['gpio_pin'])
		form = ScheduleForm(request.POST)
		# request.POST['gpio_pin']=form.cleaned_data['gpio_pin']
		if form.is_valid():
			schedule_input_list = form.cleaned_data['how_often']
			schedule_input_display = form.cleaned_data['how_often_display']
			gpio_pin=form.cleaned_data['gpio_pin']
			start_schedule.schedule_display_inputs(schedule_input_display,gpio_pin)
			for schedule_input in schedule_input_list:
				print(schedule_input)
				if gpio_pin == '18':
					how_often = {}
					how_often['hour']=schedule_input['schedule_key'][1]
					how_often['minute']=schedule_input['schedule_key'][2]
					how_often_day = schedule_input['schedule_key'][3]
					schedule_duration = schedule_input['schedule_key'][4]
					start_schedule.remove_schedule('climate_job_id',gpio_pin)
				else:
					how_often = schedule_input['schedule_key'][0]
					how_often_day = schedule_input['schedule_key'][3]
					schedule_duration = schedule_input['schedule_key'][4]

				schedule_job_id = schedule_input['job_id']
				start_schedule.add_schedule(how_often_day, how_often,schedule_duration,gpio_pin,schedule_job_id)
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

@login_required
def start_automation(request):
	if request.method == 'POST':
		start_schedule.exhaust_automation()
		return redirect('/schedule')
	else:
		return render(request, 'schedule.html')