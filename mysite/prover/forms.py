from django import forms

from .models import Directory
from .models import File


class FileUploadForm(forms.ModelForm):
    parent_dir = forms.ModelChoiceField(Directory.objects.filter(available=True))

    class Meta:
        model = File
        fields = ('file_data', 'opt_description')


class DirectoryAddForm(forms.ModelForm):
    opt_parent_dir = forms.ModelChoiceField(
        Directory.objects.filter(available=True),
        blank=True, required=False
    )

    class Meta:
        model = Directory
        fields = ('name', 'opt_description')


class DirectoryDeleteForm(forms.Form):
    target = forms.ModelChoiceField(Directory.objects.filter(available=True))


class FileDeleteForm(forms.Form):
    target = forms.ModelChoiceField(File.objects.filter(available=True))
