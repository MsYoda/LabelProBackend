from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


from rest_api.controller.dataset_controller import DatasetController
from rest_api.controller.files_controller import FilesController
from rest_api.controller.labels_controller import LabelsController



urlpatterns = [
    path("admin/action-forms/", include("django_admin_action_forms.urls")),
    path('admin/', admin.site.urls),
    path('api/task/', LabelsController.as_view()),
    path('api/file/', FilesController.as_view()),
    path('api/dataset/<int:dataset_id>/', DatasetController.as_view(),),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)