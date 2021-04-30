from django.http import HttpResponse
from django.template import loader
from django.core.files.storage import FileSystemStorage  # todo rt
from django.shortcuts import render, redirect

from django.shortcuts import reverse

from .forms import FileUploadForm
from .models import File
from .models import Directory


def index(request):
    context = {'directory_structure': Directory.get_entire_structure()}
    return render(request, 'prover/index.html', context)


def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Alter
            form.save()
            return redirect('index')
    else:
        form = FileUploadForm()
    return render(request, 'prover/upload.html', {'form': form})
