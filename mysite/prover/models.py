# Development info:
# python manage.py makemigrations prover'
# python manage.py sqlmigrate prover <#>  (optional)
# python manage.py check  (optional)
# python manage.py migrate

import pathlib
import re

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import models as auth_models


# All the entities have a timestamp and a validity flag. todo
# The actual model may contain more entities and each of the entities may have more properties.

# Directory - is an entity that holds files and other directories.
# In addition to descriptions of relations with other entities, it has:
# a name,
# an optional description,
# a creation date
# an owner
# an availability flag (false if the directory was deleted)
class Directory(models.Model):
    name = models.CharField(max_length=256)
    opt_parent_dir = models.ForeignKey(
        verbose_name='Parent dir',
        to='Directory', on_delete=models.CASCADE,
        blank=True, null=True)
    opt_description = models.CharField('optional description', max_length=256, blank=True)
    creation_date = models.DateTimeField('date created', auto_now=True)
    owner = models.ForeignKey(auth_models.User, on_delete=models.RESTRICT)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @property
    def classname(self):
        return self.__class__.__name__

    def _get_dependent_dirs_and_files(self, owner=None):
        if owner:
            dirs = Directory.objects.filter(opt_parent_dir=self.id, available=True, owner=owner)
            files = File.objects.filter(parent_dir=self.id, available=True, owner=owner)
        else:
            dirs = Directory.objects.filter(opt_parent_dir=self.id, available=True)
            files = File.objects.filter(parent_dir=self.id, available=True)

        return dirs, files

    def get_directory_structure(self, owner=None):
        dirs_set, files_set = self._get_dependent_dirs_and_files(owner)

        files = [f for f in files_set]
        dirs = [e for d in dirs_set for e in
                d.get_directory_structure(owner)]  # unpack nested lists
        structure = [self]
        if len(files) > 0:
            structure += ['#in#'] + files + ['#out#']
        if len(dirs) > 0:
            structure += ['#in#'] + dirs + ['#out#']

        return structure

    @staticmethod
    def get_entire_structure(owner=None):
        if owner:
            parentless = Directory.objects.filter(
                opt_parent_dir__isnull=True, available=True, owner=owner)
        else:
            parentless = Directory.objects.filter(opt_parent_dir__isnull=True, available=True)
        return [e for d in parentless for e in
                d.get_directory_structure(owner)]  # unpack nested lists

    # marks this and depended objects as not available
    def disable(self):
        dirs_set, files_set = self._get_dependent_dirs_and_files()

        for d in dirs_set:
            d.disable()
        for f in files_set:
            f.disable()

        self.available = False
        self.save(update_fields=['available'])  # todo Is this tokay?


# File - is an entity that contains a source code, the source code is divided into sections.
# In addition to descriptions of relations with other entities, it has:
# a name,
# an optional description,
# a creation date,
# an owner
# an availability flag (false if the file was deleted)
class File(models.Model):
    # todo DRY?
    file_data = models.FileField(upload_to='uploads/')  # todo change this dir to user-specific?
    parent_dir = models.ForeignKey(Directory, on_delete=models.CASCADE)
    opt_description = models.CharField('optional description', max_length=256, blank=True)
    creation_date = models.DateTimeField('date created', auto_now=True)
    owner = models.ForeignKey(auth_models.User, on_delete=models.RESTRICT)
    available = models.BooleanField(default=True)

    @property
    def name(self):
        return pathlib.Path(self.file_data.name).name  # todo Something more efficient?

    @property
    def classname(self):
        return self.__class__.__name__

    def __str__(self):
        return self.name

    def disable(self):
        self.available = False
        self.save(update_fields=['available'])  # todo Is this the proper way?


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

    # Status data - is an entity that defines data associated with the section status,
    # e.g. the counterexample content, the name of the solver that proved validity (e.g. Z3, CVC4 etc.).
    # a status data field
    # a user
    class StatusData(models.Model):
        prover_name = models.CharField(max_length=32, blank=True)
        user = models.ForeignKey(auth_models.User, on_delete=models.RESTRICT)

    opt_name = models.CharField('optional name', max_length=256, blank=True)
    opt_description = models.CharField('optional description', max_length=256, blank=True)
    creation_date = models.DateTimeField('date created')
    section_category = models.CharField(max_length=4, choices=SectionCategory.choices)
    status = models.CharField(max_length=2, choices=SectionStatus.choices)
    status_data = StatusData()  # todo Is the current impl ok?

    class Range:
        def __init__(self, _lines=None, _status=None, _name=None):
            self.lines = _lines
            self.status = _status
            self.name = _name

        @property
        def classname(self):
            return self.__class__.__name__

    @staticmethod
    def _first_occurrence_index(pattern, lines):
        for index, line in enumerate(lines):
            if re.match(pattern, line):
                return index
        return len(lines)

    # Pomysł: Parsuję ("tnę") wyjście z framy w sekcje zapisując w nich surowy tekst
    # oraz wyciągnięte dane, a następnie używam tych informacji do wyświetlenia sparsowanych
    # rezultatów.

    @staticmethod
    def _parse_procedure_subsection(combined):
        match = re.match(R'.*Prover (.*) returns (.*?)(( .*)|$)', combined, re.DOTALL)
        status = match.group(2) if match else None
        split = list(filter(None, combined.split('\n')))
        return FileSection.Range(split, status, split[0])

    @staticmethod
    def _all_valid(parsed):
        return all(map(lambda x: x == '#out#' or x.status == 'Valid', parsed))

    @staticmethod
    def _parse_procedure(procedure_name, combined):
        # parse subsections
        # create overall status based on subsection statuses
        parsed = []
        for sub in re.finditer('(.*?)\n-{60}', combined, re.DOTALL):
            parsed += [FileSection._parse_procedure_subsection(sub.group(1))]

        parent = FileSection.Range(
            [],
            'Valid' if FileSection._all_valid(parsed) else 'Invalid',
            procedure_name)
        return [parent, '#in#'] + parsed + ['#out#']

    @staticmethod
    def _parse_remaining(remaining_lines):
        combined = '\n'.join(remaining_lines)
        pattern = '-{60}\n.*(Function .+)\n-{60}'
        split = re.split(pattern, combined)

        parsed = []
        for index, elem in enumerate(split):
            if re.match(R'^\s*Function.*', elem):
                procedure_content = split[index + 1] if index < len(split) else None
                parsed += FileSection._parse_procedure(elem, procedure_content)

        return parsed

    @staticmethod
    def parse_from_frama_output(frama_output):
        # sekcja-rodzic to dane od początku wyjścia do pierwszej podsekcji albo końca pliku
        lines = frama_output.split('\n')
        index = FileSection._first_occurrence_index('^-+$', lines)

        remaining = FileSection._parse_remaining(lines[index:])
        overview = FileSection.Range(lines[:index], 'N_A', 'overview')

        return [overview] + remaining
