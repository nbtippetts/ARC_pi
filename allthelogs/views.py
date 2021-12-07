from django.shortcuts import render, redirect
import csv
from django.http import HttpResponse, response
from django.contrib.auth.decorators import login_required
from .forms import GetLogsForm
from .models import SelectLogs
from schedule.models import ScheduleLog
from climate.models import ClimateLogs

# Create your views here.
def logging_view(request):
	return render(request, 'allthelogs.html')

@login_required
def download_schedule_csv(request, *args, **kwargs):
	response = HttpResponse(content_type='text/csv')
	cd = f'attachment; filename=schedule_logs.csv'
	response['Content-Disposition'] = cd
	fieldnames = ('start','duration','finish_date','start_date','gpio_pin',)
	data=ScheduleLog.objects.values(*fieldnames)
	writer = csv.DictWriter(response, fieldnames=fieldnames)
	writer.writeheader()
	for row in data:
		writer.writerow(row)
	return response

@login_required
def download_climate_csv(request, *args, **kwargs):
	response = HttpResponse(content_type='text/csv')
	cd = f'attachment; filename=climate_logs.csv'
	response['Content-Disposition'] = cd
	fieldnames = ('humidity','temp','vpd','created_at')
	data=ClimateLogs.objects.values(*fieldnames)
	writer = csv.DictWriter(response, fieldnames=fieldnames)
	writer.writeheader()
	for row in data:
		writer.writerow(row)
	return response
@login_required
def select_logs(request):
	if request.method == 'POST':
		form = GetLogsForm(request.POST)
		if form.is_valid():
			start_log=form.cleaned_data['start_log']
			end_log=form.cleaned_data['end_log']
			gpio_pin=form.cleaned_data['gpio_pin_date_range']
			try:
				date_logs = SelectLogs.objects.get(gpio_pin=int(gpio_pin))
				date_logs.start_date=start_log
				date_logs.end_date=end_log
				date_logs.gpio_pin=gpio_pin
				date_logs.save()
			except SelectLogs.DoesNotExist:
				date_logs=SelectLogs()
				date_logs.start_date=start_log
				date_logs.end_date=end_log
				date_logs.gpio_pin=gpio_pin
				date_logs.save()
				pass
			context = {
				'daterange_form':form,
			}
			return redirect('/allthelogs', context)
	else:
		form = GetLogsForm()

	context = {
		'daterange_form': form
	}
	return render(request, 'allthelogs.html',context)
