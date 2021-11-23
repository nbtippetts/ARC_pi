from django.http import JsonResponse
import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import ClimateLogs, ClimateValues, Exhaust
from .forms import ClimateValuesForm, ExhaustForm
from schedule.forms import GetLogsForm
from schedule.models import ScheduleDateLog
from django.contrib.auth.decorators import login_required

@login_required
def download_climate_csv(request, *args, **kwargs):
	response = HttpResponse(content_type='text/csv')
	cd = f'attachment; filename=climate_logs.csv'
	response['Content-Disposition'] = cd
	fieldnames = ('humidity','temp','created_at')
	data=ClimateLogs.objects.values(*fieldnames)
	writer = csv.DictWriter(response, fieldnames=fieldnames)
	writer.writeheader()
	for row in data:
		writer.writerow(row)
	return response

@login_required
def select_climate_logs(request):
	if request.method == 'POST':
		form = GetLogsForm(request.POST)
		if form.is_valid():
			start_log=form.cleaned_data['start_log']
			end_log=form.cleaned_data['end_log']
			gpio_pin=4
			try:
				date_logs = ScheduleDateLog.objects.get(gpio_pin=int(gpio_pin))
				date_logs.start_date=start_log
				date_logs.end_date=end_log
				date_logs.gpio_pin=gpio_pin
				date_logs.save()
			except ScheduleDateLog.DoesNotExist:
				date_logs=ScheduleDateLog()
				date_logs.start_date=start_log
				date_logs.end_date=end_log
				date_logs.gpio_pin=gpio_pin
				date_logs.save()
				pass
			context = {
				'daterange_form':form,
			}
			return redirect('/climate', context)
	else:
		form = GetLogsForm()

	context = {
		'daterange_form': form
	}
	return render(request, 'schedule.html',context)
@login_required
def climate(request):
	return render(request, 'climate.html')

@login_required
def set_climate(request):
	if request.method == 'POST':
		form = ClimateValuesForm(request.POST)
		if form.is_valid():
			day_values = ClimateValues.objects.get(pk=1)
			day_values.humidity_value = form.cleaned_data['humidity_value_day']
			day_values.buffer_value = form.cleaned_data['buffer_value_day']
			day_values.temp_value = form.cleaned_data['temp_value_day']
			day_values.save()

			night_values = ClimateValues.objects.get(pk=2)
			night_values.humidity_value = form.cleaned_data['humidity_value_night']
			night_values.buffer_value = form.cleaned_data['buffer_value_night']
			night_values.temp_value = form.cleaned_data['temp_value_night']
			night_values.start_time = form.cleaned_data['start_time']
			night_values.end_time = form.cleaned_data['end_time']
			night_values.save()
			print('Humidity and temperature values saved successfully.')
			# ht_obj = ClimateLogs.objects.all().order_by('-created_at')[:10]
			context = {'form':form}
			return redirect('/climate',context)
	else:
		form = ClimateValuesForm()
	# ht_obj = ClimateLogs.objects.all().order_by('-created_at')[:10]
	context = {'form':form}
	return render(request, 'climate.html',context)
