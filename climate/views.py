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
			data = ClimateValues.objects.get(pk=1)
			data.humidity_value = form.cleaned_data['humidity_value']
			data.buffer_value = form.cleaned_data['buffer_value']
			data.temp_value = form.cleaned_data['temp_value']
			data.save()
			print('Humidity and temperature values saved successfully.')
			ht_obj = ClimateLogs.objects.all().order_by('-created_at')[:10]
			context = {'data': ht_obj,'form':form}
			return render(request, 'climate.html',context)

		ht_obj = ClimateLogs.objects.all().order_by('-created_at')[:10]
		context = {'data': ht_obj,'form':form}
		return render(request, 'climate.html',context)
