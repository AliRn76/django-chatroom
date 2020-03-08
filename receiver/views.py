from django.shortcuts import render, redirect

from receiver.forms import DocumentForm


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('.')
    else:
        form = DocumentForm()

    return render(request, 'model_form_upload.html', {'form': form})