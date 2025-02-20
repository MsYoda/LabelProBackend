from abc import ABC, abstractmethod
from typing import BinaryIO

class DatasetRepository(ABC):
    @abstractmethod
    def create_dataset_files(self, file: BinaryIO, dataset_name: str) -> None:
        pass

    @abstractmethod
    def get_files_count(self, dataset_name: str) -> int:
        pass
