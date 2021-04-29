from django.contrib import admin

from .models import File
from .models import Directory

admin.site.register(File)
admin.site.register(Directory)
