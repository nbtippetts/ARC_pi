from django.http import JsonResponse
from django.shortcuts import render
from .models import ClimateLogs, ClimateValues, Exhaust
from .forms import ClimateValuesForm, ExhaustForm
from django.contrib.auth.decorators import login_required

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
			ht_obj = ClimateLogs.objects.all().order_by('-created_at')[:10]
			context = {'data': ht_obj,'form':form}
			return render(request, 'climate.html',context)

		ht_obj = ClimateLogs.objects.all().order_by('-created_at')[:10]
		context = {'data': ht_obj,'form':form}
		return render(request, 'climate.html',context)
