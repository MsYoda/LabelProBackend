from django.apps import AppConfig



class RestApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rest_api'

    def ready(self):
        from .data.datasource.dataset_files_source import DatasetFilesDatasource
        from .data.datasource.labels_mongo_source import LabelsMongoDatasource
        from .data.datasource.dataset_db_source import DatasetDBSource
        from .domain.repository.dataset_repository import DatasetRepository
        from .domain.repository.label_repository import LabelRepository
        from .data.repository_impl.dataset_repository_impl import DatasetRepositoryImpl
        from .di.service_locator import ServiceLocator
        from .data.repository_impl.label_repository_impl import LabelRepositoryImpl
 
        
        ServiceLocator.register(DatasetFilesDatasource, DatasetFilesDatasource())
        ServiceLocator.register(LabelsMongoDatasource, LabelsMongoDatasource())
        ServiceLocator.register(DatasetDBSource, DatasetDBSource())

        ServiceLocator.register(DatasetRepository, DatasetRepositoryImpl(
            files_source=ServiceLocator.get(
                DatasetFilesDatasource
            ),
            dataset_db_source=ServiceLocator.get(DatasetDBSource),
            labels_mongo_source=ServiceLocator.get(LabelsMongoDatasource),
                )
            )
        ServiceLocator.register(LabelRepository, LabelRepositoryImpl(
            mongo_source=ServiceLocator.get(
                LabelsMongoDatasource
            )))
    
