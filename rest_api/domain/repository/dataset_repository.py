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
