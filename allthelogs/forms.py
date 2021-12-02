from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from datetime import datetime

select_gpio_pin = (
	(14, 'Lights'),
	(15, 'Water'),
	(4, 'Climate'),
	(3, 'Exhuast')
)

class GetLogsForm(forms.Form):
	date_range_picker = forms.CharField(required=False)
	gpio_pin_date_range = forms.ChoiceField(
		label=False,
		choices=select_gpio_pin
	)
	def clean(self):
		cleaned_data = super().clean()
		date_range=self.cleaned_data['date_range_picker'].split(' - ')
		self.cleaned_data['start_log']=datetime.strptime(date_range[0], '%Y-%m-%d %I:%M%p')
		self.cleaned_data['end_log']=datetime.strptime(date_range[1], '%Y-%m-%d %I:%M%p')
		print(self.cleaned_data)
