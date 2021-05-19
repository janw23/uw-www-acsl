from django import forms

from .models import Directory
from .models import File


# todo Czy taka magia jest dozwolona?
def FileUploadForm(owner, *args, **kwargs):
    class _FileUploadForm(forms.ModelForm):
        parent_dir = forms.ModelChoiceField(
            Directory.objects.filter(available=True, owner=owner))

        class Meta:
            model = File
            fields = ('file_data', 'opt_description')

    return _FileUploadForm(*args, **kwargs)


def DirectoryAddForm(owner, *args, **kwargs):
    class _DirectoryAddForm(forms.ModelForm):
        opt_parent_dir = forms.ModelChoiceField(
            Directory.objects.filter(available=True, owner=owner),
            blank=True, required=False
        )

        class Meta:
            model = Directory
            fields = ('name', 'opt_description')

    return _DirectoryAddForm(*args, **kwargs)


def DirectoryDeleteForm(owner, *args, **kwargs):
    class _DirectoryDeleteForm(forms.Form):
        target = forms.ModelChoiceField(Directory.objects.filter(available=True, owner=owner))

    return _DirectoryDeleteForm(*args, **kwargs)


def FileDeleteForm(owner, *args, **kwargs):
    class _FileDeleteForm(forms.Form):
        target = forms.ModelChoiceField(File.objects.filter(available=True, owner=owner))

    return _FileDeleteForm(*args, **kwargs)
