from django import forms
from .models import Schedule,RelayStatus
from simpleduration import Duration
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from schedule.timer_inputs import timer_hours, timer_minutes

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

select_gpio_pin = (
	(14, 'Lights'),
	(15, 'Water')
)

duration_hour = timer_hours()
duration_minute = timer_minutes()
class TimeInput(forms.TimeInput):
	input_type = 'time'


class ScheduleForm(forms.Form):
	how_often_hour = forms.TimeField(label='Run Times', widget=TimeInput)
	duration_hours = forms.ChoiceField(choices=duration_hour)
	duration_minutes = forms.ChoiceField(choices=duration_minute)
	how_often_day = forms.ChoiceField(choices=cron_job_week)

	how_often_hour1 = forms.TimeField(label='',widget=TimeInput, required=False)
	duration_hours1 = forms.ChoiceField(choices=duration_hour)
	duration_minutes1 = forms.ChoiceField(choices=duration_minute)
	how_often_day1 = forms.ChoiceField(choices=cron_job_week)

	how_often_hour2 = forms.TimeField(label='',widget=TimeInput, required=False)
	duration_hours2 = forms.ChoiceField(choices=duration_hour)
	duration_minutes2 = forms.ChoiceField(choices=duration_minute)
	how_often_day2 = forms.ChoiceField(choices=cron_job_week)

	how_often_hour3 = forms.TimeField(label='',widget=TimeInput, required=False)
	duration_hours3 = forms.ChoiceField(choices=duration_hour)
	duration_minutes3 = forms.ChoiceField(choices=duration_minute)
	how_often_day3 = forms.ChoiceField(choices=cron_job_week)

	gpio_pin = forms.ChoiceField(
		choices=select_gpio_pin
	)
	def clean(self):
		cleaned_data = super().clean()
		self.cleaned_data['how_often']=[]
		self.cleaned_data['how_often_display']=[]
		gpio_pin=self.cleaned_data['gpio_pin']
		schedule_job_id = f'update_schedule_job_id_{gpio_pin}'
		run_time_list = [
			{'job_id':f'{schedule_job_id}_0','schedule_key': [self.cleaned_data['how_often_hour'],self.cleaned_data['duration_hours'],self.cleaned_data['duration_minutes'],self.cleaned_data['how_often_day']]},
			{'job_id':f'{schedule_job_id}_1','schedule_key': [self.cleaned_data['how_often_hour1'],self.cleaned_data['duration_hours1'],self.cleaned_data['duration_minutes1'],self.cleaned_data['how_often_day1']]},
			{'job_id':f'{schedule_job_id}_2','schedule_key': [self.cleaned_data['how_often_hour2'],self.cleaned_data['duration_hours2'],self.cleaned_data['duration_minutes2'],self.cleaned_data['how_often_day2']]},
			{'job_id':f'{schedule_job_id}_3','schedule_key': [self.cleaned_data['how_often_hour3'],self.cleaned_data['duration_hours3'],self.cleaned_data['duration_minutes3'],self.cleaned_data['how_often_day3']]},
		]
		for run_time in run_time_list:
			print(run_time['schedule_key'][0])
			if run_time['schedule_key'][0] != None:
				self.cleaned_data['how_often'].append(run_time)
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
