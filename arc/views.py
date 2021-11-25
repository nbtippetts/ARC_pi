from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from schedule.forms import ScheduleForm
from datetime import datetime

def homepage(request):
	if request.user.is_authenticated:
		start = datetime.now()
		dtwithoutseconds = start.replace(second=0, microsecond=0)
		form = ScheduleForm(initial={
			'start': dtwithoutseconds
		})
		context = {
			'form': form,
		}
		return redirect('/schedule',context)
	else:
		return render(request, 'landing_page.html')
