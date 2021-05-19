from django.shortcuts import render, redirect

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django import forms

from .forms import DirectoryAddForm, DirectoryDeleteForm
from .forms import FileUploadForm, FileDeleteForm
from .models import Directory, FileSection, File

from . import frama


def _get_full_path(frama_target):
    if frama_target:
        return settings.MEDIA_ROOT / 'uploads' / frama_target
    else:
        return None


def _get_focus_window_content(target_file):
    if target_file:
        # todo Don't allow on not available files
        return FileSection.parse_from_frama_output(frama.wp_print(target_file))
    else:
        return [FileSection.Range(['You need to select a file first!'])]


def _get_editor_window_content(target_file):
    if not target_file:
        return ['']
    with open(target_file, 'r') as f:
        lines = f.readlines()
    return [line.strip('\n') for line in lines]


@login_required
def index(request, frama_target_pk=None):
    if frama_target_pk:
        frama_target = File.objects.get(pk=frama_target_pk)
        if not frama_target.available or not frama_target.owner == request.user:
            return HttpResponseBadRequest()

    target_file = _get_full_path(frama_target.name) if frama_target_pk else None

    context = {
        'directory_structure': Directory.get_entire_structure(request.user),
        'focus_content': _get_focus_window_content(target_file),
        'editor_content': _get_editor_window_content(target_file),
        'user' : request.user,
    }
    return render(request, 'prover/index.html', context)


@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            new_file = form.save(commit=False)
            new_file.parent_dir = form.cleaned_data['parent_dir']
            new_file.owner = request.user
            new_file.save()
            return redirect('index')
    else:
        form = FileUploadForm(request.user)
    return render(request, 'prover/file_upload.html', {'form': form})


@login_required
def add_directory(request):
    if request.method == 'POST':
        form = DirectoryAddForm(request.user, request.POST)
        if form.is_valid():
            new_dir = form.save(commit=False)
            new_dir.opt_parent_dir = form.cleaned_data['opt_parent_dir']
            new_dir.owner = request.user
            new_dir.save()
            return redirect('index')
    else:
        form = DirectoryAddForm(request.user)
    return render(request, 'prover/dir_add.html', {'form': form})


@login_required
def delete_dir_or_file(request):
    form_classes = {
        '/prover/file-delete': FileDeleteForm,
        '/prover/dir-delete': DirectoryDeleteForm
    }
    assert request.path in form_classes.keys()

    if request.method == 'POST':
        form = form_classes[request.path](request.user, request.POST)
        if form.is_valid():
            form.cleaned_data['target'].disable()
            return redirect('index')
    else:
        form = form_classes[request.path](request.user)

    context = {'directory_structure': Directory.get_entire_structure(request.user),
               'form': form}
    return render(request, 'prover/delete.html', context)
