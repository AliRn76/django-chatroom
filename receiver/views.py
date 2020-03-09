from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from receiver.forms import DocumentForm

from receiver.models import Document

@login_required()
def upload_view(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            upload  = form.save(commit=False)
            upload.user = request.user
            upload.save()

            last_upload = Document.objects.all().last().document.url
            last_upload = last_upload[1:]

            my_links = Document.objects.filter(user=request.user).order_by('-uploaded_at')


    else:
        form = DocumentForm()
        last_upload = ''
        my_links = Document.objects.filter(user=request.user)

    context ={
        'form': form,
        'last_upload': last_upload,
        'my_links': my_links
    }

    return render(request, 'upload.html', context)


@login_required()
def delete_file_view(request, file_number):
    my_links = Document.objects.filter(user=request.user).order_by('uploaded_at')
    my_links[file_number-1].delete()

    return redirect("/upload")