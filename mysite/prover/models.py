from django.db import models
from django.utils.translation import gettext_lazy as _


# TODO Create things and refine them gradually as you learn.

# All the entities have a timestamp and a validity flag.
# The actual model may contain more entities and each of the entities may have more properties.

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
    opt_description = models.TextField('optional description')
    creation_date = models.DateTimeField('date created')
    owner = None  # todo
    available = models.BooleanField()


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
    name = models.CharField(max_length=256)  # todo more suitable type? ask someone?
    opt_description = models.TextField('optional description')
    creation_date = models.DateTimeField('date created')
    owner = None  # todo
    available = models.BooleanField()


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
        PROVED = 'PR', _('Proved')
        INVALID = 'IN', _('Invalid')
        COUNTEREXAMPLE = 'CO', _('Counterexample')
        UNCHECKED = 'UN', _('Unchecked')

    # todo Relations
    opt_name = models.CharField(max_length=256)  # todo more suitable type? ask someone?
    opt_description = models.TextField('optional description')
    creation_date = models.DateTimeField('date created')
    section_category = models.CharField(max_length=4, choices=SectionCategory.choices)
    status = models.CharField(max_length=2, choices=SectionStatus.choices)
    status_data = None  # todo


# Status data - is an entity that defines data associated with the section status,
# e.g. the counterexample content, the name of the solver that proved validity (e.g. Z3, CVC4 etc.).
# a status data field
# a user
class StatusData(models.Model):
    # todo Should this really be a separate model?
    data = models.TextField()
    user = None  # todo


# User – is an entity that defines a user of the application.
# a name
# a login
# a password
class User(models.Model):
    name = models.CharField(max_length=32)
    login = models.CharField(max_length=16)
    password = models.CharField(max_length=32)  # todo encryption in the futue>
