from django import forms
from .models import Schedule,RelayStatus,ScheduleLog
from simpleduration import Duration
from bootstrap_datepicker_plus import DatePickerInput
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from schedule.timer_inputs import timer_hours, timer_minutes
from datetime import datetime
import pytz

on_off_gpio = (
	(True, 'Start'),
	(False, 'Stop'),
)
cron_job_week = (
	('*', 'Every Day'),
	('mon,wed,fri,sun', 'Every Other Day'),
	('mon-fri', 'Weekdays'),
	('sat-sun', 'Weekend Days'),
)
cron_job_hours = (
	('*/2', 'Every 2 Minutes'),
	('*/5', 'Every 5 Minutes'),
	('*/10', 'Every 10 Minutes'),
	('*/15', 'Every 15 Minutes'),
	('*/20', 'Every 20 Minutes'),
	('*/25', 'Every 25 Minutes'),
	('*/30', 'Every 30 Minutes'),
	('*/45', 'Every 45 Minutes'),
)

select_gpio_pin = (
	(14, 'Lights'),
	(15, 'Water'),
	(18, 'Exhuast')
)

duration_hour = timer_hours()
duration_minute = timer_minutes()
class TimeInput(forms.TimeInput):
	input_type = 'time'


class ScheduleForm(forms.Form):
	run_time_input = forms.TimeField(label='Run Times', widget=TimeInput,required=False)
	duration_hours = forms.ChoiceField(choices=duration_hour,required=False)
	duration_minutes = forms.ChoiceField(choices=duration_minute,required=False)
	how_often_day = forms.ChoiceField(choices=cron_job_week,required=False)

	run_time_input1 = forms.TimeField(label='',widget=TimeInput, required=False)
	duration_hours1 = forms.ChoiceField(choices=duration_hour,required=False)
	duration_minutes1 = forms.ChoiceField(choices=duration_minute,required=False)
	how_often_day1 = forms.ChoiceField(choices=cron_job_week,required=False)

	run_time_input2 = forms.TimeField(label='',widget=TimeInput, required=False)
	duration_hours2 = forms.ChoiceField(choices=duration_hour,required=False)
	duration_minutes2 = forms.ChoiceField(choices=duration_minute,required=False)
	how_often_day2 = forms.ChoiceField(choices=cron_job_week,required=False)

	run_time_input3 = forms.TimeField(label='',widget=TimeInput, required=False)
	duration_hours3 = forms.ChoiceField(choices=duration_hour,required=False)
	duration_minutes3 = forms.ChoiceField(choices=duration_minute,required=False)
	how_often_day3 = forms.ChoiceField(choices=cron_job_week,required=False)

	run_time_input4 = forms.ChoiceField(choices=cron_job_hours,required=False)
	duration_hours4 = forms.ChoiceField(choices=duration_hour,required=False)
	duration_minutes4 = forms.ChoiceField(choices=duration_minute,required=False)

	gpio_pin = forms.ChoiceField(
		choices=select_gpio_pin,
		required=False
	)
	# gpio_pin_18 = forms.CharField(widget = forms.HiddenInput(), required = False)
	def clean(self):
		cleaned_data = super().clean()
		self.cleaned_data['how_often']=[]
		self.cleaned_data['how_often_display']=[]
		gpio_pin=self.cleaned_data['gpio_pin']
		schedule_job_id = f'update_schedule_job_id_{gpio_pin}'
		if gpio_pin == '18':
			run_time_list = [
				{'job_id':f'{schedule_job_id}','schedule_key': [datetime.now().time(),self.cleaned_data['duration_hours4'],self.cleaned_data['duration_minutes4'],self.cleaned_data['run_time_input4']]},
			]
		else:
			run_time_list = [
				{'job_id':f'{schedule_job_id}_0','schedule_key': [self.cleaned_data['run_time_input'],self.cleaned_data['duration_hours'],self.cleaned_data['duration_minutes'],self.cleaned_data['how_often_day']]},
				{'job_id':f'{schedule_job_id}_1','schedule_key': [self.cleaned_data['run_time_input1'],self.cleaned_data['duration_hours1'],self.cleaned_data['duration_minutes1'],self.cleaned_data['how_often_day1']]},
				{'job_id':f'{schedule_job_id}_2','schedule_key': [self.cleaned_data['run_time_input2'],self.cleaned_data['duration_hours2'],self.cleaned_data['duration_minutes2'],self.cleaned_data['how_often_day2']]},
				{'job_id':f'{schedule_job_id}_3','schedule_key': [self.cleaned_data['run_time_input3'],self.cleaned_data['duration_hours3'],self.cleaned_data['duration_minutes3'],self.cleaned_data['how_often_day3']]},
			]
		for run_time in run_time_list:
			print(run_time['schedule_key'][0])
			if run_time['schedule_key'][0] != None:
				self.cleaned_data['how_often'].append(run_time)
				if gpio_pin == '18':
					exhaust_run=self.cleaned_data.get('run_time_input4')
					exhaust_run_time=dict(self.fields['run_time_input4'].choices)[exhaust_run]
					print(exhaust_run_time)
					self.cleaned_data['how_often_display'].append((run_time['schedule_key'][0].strftime("%I:%M:%p"),run_time['schedule_key'][1],run_time['schedule_key'][2],run_time['job_id'],run_time['schedule_key'][3]))
				else:
					self.cleaned_data['how_often_display'].append((run_time['schedule_key'][0].strftime("%I:%M:%p"),run_time['schedule_key'][1],run_time['schedule_key'][2],run_time['job_id']))
		print(self.cleaned_data['how_often'])
		for often in self.cleaned_data['how_often']:
			duration_hours = often['schedule_key'][1]
			duration_minutes = often['schedule_key'][2]
			duration=Duration(f"{duration_hours} hour {duration_minutes} minute")
			duration=duration.timedelta()
			often['schedule_key'].append(duration)
		print(self.cleaned_data['how_often'])
		# how_often = self.cleaned_data['how_often']
		# if how_often.seconds == 0:
		# 	print('24 Hours')
		# elif self.cleaned_data['duration'].seconds >= how_often.seconds:
		# 	raise forms.ValidationError("Duration must be less then how often")
		# else:
		# 	print('something else went wrong')
	class Meta:
		model = Schedule

class RemoveScheduleForm(forms.Form):
	gpio_pin = forms.ChoiceField(
		label=False,
		choices=select_gpio_pin
	)
class RelayStatusForm(forms.Form):
	class Meta:
		model = RelayStatus

class DateInput(forms.DateInput):
	input_type='date'

class GetLogsForm(forms.Form):
	date_range_picker = forms.CharField(required=False)
	# start_log=forms.DateTimeField(widget=DateInput())
	# end_log=forms.DateTimeField(widget=DateInput())
	gpio_pin = forms.ChoiceField(
		label=False,
		choices=select_gpio_pin
	)
	def clean(self):
		cleaned_data = super().clean()
		date_range=self.cleaned_data['date_range_picker'].split(' - ')
		self.cleaned_data['start_log']=datetime.strptime(date_range[0], '%Y-%m-%d %I:%M%p')
		self.cleaned_data['end_log']=datetime.strptime(date_range[1], '%Y-%m-%d %I:%M%p')
		print(self.cleaned_data)
		# start_date_range=date_range[0].split('-')
		# end_date_range=date_range[1].split('-')
		# self.cleaned_data['start_log']=f"{start_date_range[2]}-{start_date_range[0]}-{start_date_range[1]}"
		# self.cleaned_data['end_log']=f"{end_date_range[2]}-{end_date_range[0]}-{end_date_range[1]}"
