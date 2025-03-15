from abc import ABC, abstractmethod
from typing import BinaryIO

from rest_api.domain.models.dataset import Dataset

class DatasetRepository(ABC):
    @abstractmethod
    def create_dataset_files(self, file: BinaryIO, dataset_name: str, folder: str) -> tuple[str, list[str]]:
        pass

    @abstractmethod
    def get_files_count(self, dataset: Dataset) -> int:
        pass

    @abstractmethod
    def get_new_task(self, dataset_id: int, user_id: int):
        pass

    @abstractmethod
    def submit_task(self, id_in_file: int, dataset_id: int, user_id: int, file_path: str, data: dict):
        pass

    @abstractmethod
    def get_dataet_by_id(self, dataset_id: int):
        pass
