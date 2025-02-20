from django.apps import AppConfig

from rest_api.data.datasource.dataset_files_source import DatasetFilesDatasource
from rest_api.domain.repository.dataset_repository import DatasetRepository
from rest_api.data.repository_impl.dataset_repository_impl import DatasetRepositoryImpl
from .di.service_locator import ServiceLocator

class RestApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rest_api'
    ServiceLocator.register(DatasetFilesDatasource, DatasetFilesDatasource())
    ServiceLocator.register(DatasetRepository, DatasetRepositoryImpl(
        files_source=ServiceLocator.get(
            DatasetFilesDatasource
        )))
    
