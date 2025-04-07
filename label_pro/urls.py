from django.contrib import admin
from django.urls import path

from rest_api.controller.dataset_controller import DatasetController
from rest_api.controller.files_controller import FilesController
from rest_api.controller.labels_controller import LabelsController



urlpatterns = [
    path('admin/', admin.site.urls),
    path('task/', LabelsController.as_view()),
    path('file/', FilesController.as_view()),
    path('dataset/<int:dataset_id>/', DatasetController.as_view(),)
]
