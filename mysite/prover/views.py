from django.shortcuts import render, redirect

from django.conf import settings

from .forms import DirectoryAddForm, DirectoryDeleteForm
from .forms import FileUploadForm, FileDeleteForm
from .models import Directory

from . import frama


def _get_focus_window_content(target_file=None):
    if target_file:
        # todo Don't allow on not available files
        frama_stdout, _ = frama.wp_print(
            settings.MEDIA_ROOT / 'uploads' / target_file)
    else:
        frama_stdout = ['You need to select a file first!']

    return frama_stdout


def index(request, frama_target=None):
    context = {
        'directory_structure': Directory.get_entire_structure(),
        'focus_content': _get_focus_window_content(frama_target),
    }
    return render(request, 'prover/index.html', context)


def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = form.save(commit=False)
            new_file.parent_dir = form.cleaned_data['parent_dir']
            new_file.save()
            return redirect('index')
    else:
        form = FileUploadForm()
    return render(request, 'prover/file_upload.html', {'form': form})


def add_directory(request):
    if request.method == 'POST':
        form = DirectoryAddForm(request.POST)
        if form.is_valid():
            new_dir = form.save(commit=False)
            new_dir.opt_parent_dir = form.cleaned_data['opt_parent_dir']
            new_dir.save()
            return redirect('index')
    else:
        form = DirectoryAddForm()
    return render(request, 'prover/dir_add.html', {'form': form})


def delete_dir_or_file(target_type, request):
    form_classes = {
        'file': FileDeleteForm,
        'dir': DirectoryDeleteForm
    }
    assert target_type in form_classes.keys()

    if request.method == 'POST':
        form = form_classes[target_type](request.POST)
        if form.is_valid():
            form.cleaned_data['target'].disable()
            return redirect('index')
    else:
        form = form_classes[target_type]()

    context = {'directory_structure': Directory.get_entire_structure(),
               'form': form}
    return render(request, 'prover/delete.html', context)
