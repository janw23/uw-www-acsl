from functools import partial

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('frama/<int:frama_target_pk>', views.index, name='index-frama-target'),
    path('file-upload', views.upload_file, name='file-upload'),
    path('dir-add', views.add_directory, name='dir-add'),
    path('dir-delete', views.delete_dir_or_file, name='dir-delete'),
    path('file-delete', views.delete_dir_or_file, name='file-delete'),
    path('ajax/select-file', views.ajax_selected_file),
]
