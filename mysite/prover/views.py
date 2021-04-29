from django.http import HttpResponse
from django.template import loader
from django.core.files.storage import FileSystemStorage  # todo rt
from django.shortcuts import render, redirect

from django.shortcuts import reverse

from .forms import FileUploadForm
from .models import File


def index(request):
    return render(request, 'prover/index.html', None)


def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = FileUploadForm()
    return render(request, 'prover/upload.html', {'form': form})
