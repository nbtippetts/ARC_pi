from django import forms
from .models import Schedule,RelayStatus
from simpleduration import Duration
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

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

class TimeInput(forms.TimeInput):
	input_type = 'time'


class ScheduleForm(forms.Form):
	start = forms.TimeField(
		widget=TimeInput
	)
	duration_hours = forms.CharField(label='Duration',widget=forms.TextInput(attrs={'placeholder': 'Hours'}),required=False)
	duration_minutes = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Minutes'}),required=False)
	duration_seconds = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Seconds'}),required=False)

	# how_often_week = forms.CharField(label='How Often',widget=forms.TextInput(attrs={'placeholder': 'Week'}))
	how_often_day = forms.ChoiceField(
		label='How Often',
		choices=cron_job_week,
		widget=forms.RadioSelect
	)
	how_often_hour = forms.TimeField(label='Run Times', widget=TimeInput)
	how_often_hour1 = forms.TimeField(label='',widget=TimeInput, required=False)
	how_often_hour2 = forms.TimeField(label='',widget=TimeInput, required=False)
	how_often_hour3 = forms.TimeField(label='',widget=TimeInput, required=False)
	# how_often = forms.DurationField(widget=forms.TextInput(attrs={'placeholder': '24 Hour Format 00:00:00'}))
	gpio_pin = forms.ChoiceField(
		choices=select_gpio_pin
	)
	def clean(self):
		cleaned_data = super().clean()
		if self.cleaned_data['duration_hours'] == '':
			duration_hours = '0'
		else:
			duration_hours = self.cleaned_data['duration_hours']
		if self.cleaned_data['duration_minutes'] == '':
			duration_minutes = '0'
		else:
			duration_minutes = self.cleaned_data['duration_minutes']
		if self.cleaned_data['duration_seconds'] == '':
			duration_seconds = '0'
		else:
			duration_seconds = self.cleaned_data['duration_seconds']

		self.cleaned_data['duration']=Duration(f"{duration_hours} hour {duration_minutes} minute {duration_seconds} second")
		self.cleaned_data['duration']=self.cleaned_data['duration'].timedelta()
		self.cleaned_data['how_often']=[]
		self.cleaned_data['how_often_display']=[]
		run_time_list = [
			self.cleaned_data['how_often_hour'],
			self.cleaned_data['how_often_hour1'],
			self.cleaned_data['how_often_hour2'],
			self.cleaned_data['how_often_hour3'],
		]
		for run_time in run_time_list:
			if run_time != None:
				self.cleaned_data['how_often'].append(run_time)
				self.cleaned_data['how_often_display'].append(run_time.strftime("%I:%M:%p"))
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
		choices=select_gpio_pin
	)
class RelayStatusForm(forms.Form):
	# status = forms.ChoiceField(
	# 	label=False,
	# 	choices=on_off_gpio,
	# 	widget=forms.RadioSelect
	# )
	class Meta:
		model = RelayStatus
		fields = ('ON','OFF')
		widgets = {
			'ON': forms.TextInput(attrs={'class': 'form-control'}),
			'OFF': forms.TextInput(attrs={'class': 'form-control'})
		}