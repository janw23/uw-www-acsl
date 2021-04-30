# Development info:
# python manage.py makemigrations prover'
# python manage.py sqlmigrate prover <#>  (optional)
# python manage.py check  (optional)
# python manage.py migrate

import pathlib

from django.db import models
from django.utils.translation import gettext_lazy as _


# TODO Create things and refine them gradually as you learn.

# All the entities have a timestamp and a validity flag. todo
# The actual model may contain more entities and each of the entities may have more properties.


# User – is an entity that defines a user of the application.
# a name
# a login
# a password
class User(models.Model):
    name = models.CharField(max_length=32)
    login = models.CharField(max_length=16)
    password = models.CharField(max_length=32)  # todo encryption in the futue?


# Directory - is an entity that holds files and other directories.
# In addition to descriptions of relations with other entities, it has:
# a name,
# an optional description,
# a creation date
# an owner
# an availability flag (false if the directory was deleted)
class Directory(models.Model):
    # todo relations
    name = models.CharField(max_length=256)  # todo more suitable type? ask someone?
    opt_parent_dir = models.ForeignKey(
        to='Directory', on_delete=models.CASCADE,
        blank=True, null=True)
    opt_description = models.TextField('optional description', blank=True)
    creation_date = models.DateTimeField('date created')
    owner = None  # todo
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_directory_structure(self):
        dirs_set = Directory.objects.filter(opt_parent_dir=self.id)
        files_set = File.objects.filter(parent_dir=self.id)

        files = [f.name for f in files_set]
        dirs = [e for d in dirs_set for e in d.get_directory_structure()]  # unpack nested lists

        structure = [self.name]
        if len(files) > 0:
            structure += ['#in#'] + files + ['#out#']
        if len(dirs) > 0:
            structure += ['#in#'] + dirs + ['#out#']

        return structure

    @staticmethod
    def get_entire_structure():
        parentless = Directory.objects.filter(opt_parent_dir__isnull=True)
        return [e for d in parentless for e in d.get_directory_structure()]  # unpack nested lists


# File - is an entity that contains a source code, the source code is divided into sections.
# In addition to descriptions of relations with other entities, it has:
# a name,
# an optional description,
# a creation date,
# an owner
# an availability flag (false if the file was deleted)
class File(models.Model):
    # todo DRY?
    # todo Relations
    file_data = models.FileField(upload_to='uploads/')  # todo change this dir to user-specific?
    parent_dir = models.ForeignKey(Directory, on_delete=models.CASCADE)
    opt_description = models.CharField('optional description', max_length=256, blank=True)
    creation_date = models.DateTimeField('date created', auto_now=True)
    owner = None  # todo
    available = models.BooleanField(default=True)

    @property
    def name(self):
        return pathlib.Path(self.file_data.name).name  # todo Something more efficient?

    def __str__(self):
        return self.name


# File section - is an entity that contains a meaningful piece of code within a file or comments;
# some file sections may contain subsections.
# In addition to descriptions of relations with other entities, it has:
# an optional name,
# an optional description,
# a creation date,
# a section category,
# a status,
# status data
class FileSection(models.Model):
    # Section category - is an entity that defines the type of a section;
    # category defines the way the file section is handled by the application.
    # Possible section categories are:
    # procedure, property, lemma, assertion, invariant, precondition, postcondition;
    # some file sections may contain subsections.
    class SectionCategory(models.TextChoices):
        PROCEDURE = 'PROC', _('Procedure')
        PROPERTY = 'PROP', _('Property')
        LEMMA = 'LEM', _('Lemma')
        ASSERTION = 'ASS', _('Assertion')
        INVARIANT = 'INV', _('Invariant')
        PRECONDITION = 'PRE', _('Precondition')
        POSTCONDITION = 'POST', _('Postcondition')

    # Section status - is an entity that defines the status of a section;
    # example status' are: proved, invalid, counterexample, unchecked.
    class SectionStatus(models.TextChoices):
        # todo Is this a proper way to implement this entity?
        # todo I can just provide a tuple and use choices as kwarg. Same with the above
        PROVED = 'PR', _('Proved')
        INVALID = 'IN', _('Invalid')
        COUNTEREXAMPLE = 'CO', _('Counterexample')
        UNCHECKED = 'UN', _('Unchecked')

    # todo Relations
    opt_name = models.CharField('optional name', max_length=256, blank=True)
    opt_description = models.CharField('optional description', max_length=256, blank=True)
    creation_date = models.DateTimeField('date created')
    section_category = models.CharField(max_length=4, choices=SectionCategory.choices)
    status = models.CharField(max_length=2, choices=SectionStatus.choices)
    # status_data = None  # todo Is the current impl ok?


# Status data - is an entity that defines data associated with the section status,
# e.g. the counterexample content, the name of the solver that proved validity (e.g. Z3, CVC4 etc.).
# a status data field
# a user
class StatusData(models.Model):
    # todo Should this really be a separate model?
    file_section = models.OneToOneField(
        FileSection,
        on_delete=models.CASCADE,
        related_name='parent_file_section'
    )
    data = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
