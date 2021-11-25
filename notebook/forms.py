from django import forms
from .models import NoteBooks
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class NoteBookForm(forms.Form):
	title = forms.CharField(label='Title',max_length=255)
	body = forms.CharField(widget=forms.Textarea)
	def clean(self):
		cleaned_data = super().clean()
	class Meta:
		model = NoteBooks