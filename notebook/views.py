from django.shortcuts import redirect, render
from .models import NoteBooks
from .forms import NoteBookForm
from datetime import date
# Create your views here.
def notebook_view(request):
	form = NoteBookForm()
	get_notes = NoteBooks.objects.order_by('-publish_date')[:25]
	for note in get_notes:
		note.publish_date = note.publish_date.strftime('%B %d, %Y')
	context = {
		"notes": get_notes,
		"form": form
	}
	return render(request, 'notebook.html',context)
def publish_note(request):
	if request.method == 'POST':
		form = NoteBookForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data['title']
			body = form.cleaned_data['body']
			save_note=NoteBooks()
			save_note.title=title
			save_note.body=body
			save_note.save()
			context = {
				'form': form
			}
			return redirect('/notebook', context)
	else:
		form = NoteBookForm()
	context = {
		'form': form
	}
	return render(request, 'notebook.html',context)
def delete_note(request):
	return render(request, 'notebook.html')
def update_notebook(request):
	return render(request, 'notebook.html')