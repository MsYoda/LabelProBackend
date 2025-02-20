
from typing import BinaryIO
from rest_api.data.datasource.dataset_files_source import DatasetFilesDatasource
from rest_api.domain.repository.dataset_repository import DatasetRepository


class DatasetRepositoryImpl(DatasetRepository):
    def __init__(self, files_source):
        self.files_source : DatasetFilesDatasource = files_source

    def create_dataset_files(self, file: BinaryIO, dataset_name: str) -> None:
        return self.files_source.create_dataset_files(file, dataset_name=dataset_name)

    def get_files_count(self, dataset_name: str) -> int:
        return self.files_source.get_files_count(dataset_name=dataset_name)
    