from django.contrib import admin
from django.urls import path

from rest_api.controller.files_controller import FilesController
from rest_api.controller.labels_controller import LabelsController



urlpatterns = [
    path('admin/', admin.site.urls),
    path('label/', LabelsController.as_view()),
    path('file/', FilesController.as_view()),
]
