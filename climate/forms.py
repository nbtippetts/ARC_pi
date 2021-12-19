from django import forms
from .models import ClimateValues, Exhaust
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

on_off_gpio = (
	(True, 'Start'),
	(False, 'Stop'),
)
class TimeInput(forms.TimeInput):
	input_type = 'time'

class ClimateValuesForm(forms.Form):
	co2_value_day = forms.DecimalField(max_digits=6, decimal_places=2,widget=forms.TextInput(attrs={'placeholder': 'DayTime CO2'}))
	co2_buffer_value = forms.DecimalField(max_digits=6, decimal_places=2,widget=forms.TextInput(attrs={'placeholder': 'CO2 Buffer'}))

	humidity_value_day = forms.DecimalField(max_digits=6, decimal_places=2,widget=forms.TextInput(attrs={'placeholder': 'DayTime Humidity'}))
	temp_value_day = forms.DecimalField(max_digits=6, decimal_places=2,widget=forms.TextInput(attrs={'placeholder': 'DayTime Temperature'}))
	buffer_value_day = forms.DecimalField(max_digits=6, decimal_places=2,widget=forms.TextInput(attrs={'placeholder': 'DayTime Buffer'}))

	humidity_value_night = forms.DecimalField(max_digits=6, decimal_places=2,widget=forms.TextInput(attrs={'placeholder': 'NightTime Humidity'}))
	temp_value_night = forms.DecimalField(max_digits=6, decimal_places=2,widget=forms.TextInput(attrs={'placeholder': 'NightTime Temperature'}))
	buffer_value_night = forms.DecimalField(max_digits=6, decimal_places=2,widget=forms.TextInput(attrs={'placeholder': 'NightTime Buffer'}))
	
	start_time = forms.TimeField(widget=TimeInput)
	end_time = forms.TimeField(widget=TimeInput)
	def clean(self):
		cleaned_data = super().clean()

	class Meta:
		model = ClimateValues

class ExhaustForm(forms.Form):
	# status = forms.ChoiceField(
	# 	label=False,
	# 	widget=forms.Select(attrs={'class':'bootstrap-select'}),
	# 	choices=on_off_gpio
	# )
	class Meta:
		model = Exhaust
		fields = ('ON','OFF', 'auto_on', 'auto_off')
		widgets = {
			'ON': forms.TextInput(attrs={'class': 'form-control'}),
			'OFF': forms.TextInput(attrs={'class': 'form-control'}),
			'auto_on': forms.TextInput(attrs={'class': 'form-control'}),
			'auto_off': forms.TextInput(attrs={'class': 'form-control'})
		}