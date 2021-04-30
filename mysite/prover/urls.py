from functools import partial

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('uploads/<path:frama_target>', views.index, name='index-frama-target'),
    path('file-upload', views.upload_file, name='file-upload'),
    path('dir-add', views.add_directory, name='dir-add'),
    path('dir-delete', partial(views.delete_dir_or_file, 'dir'), name='dir-delete'),
    path('file-delete', partial(views.delete_dir_or_file, 'file'), name='file-delete'),
]
