from django import forms
from .models import ClimateValues, Exhaust
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

on_off_gpio = (
	(True, 'Start'),
	(False, 'Stop'),
)

class ClimateValuesForm(forms.Form):
	humidity_value = forms.DecimalField(max_digits=6, decimal_places=2)
	buffer_value = forms.DecimalField(max_digits=6, decimal_places=2)
	temp_value = forms.DecimalField(max_digits=6, decimal_places=2)
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