from abc import ABC, abstractmethod


class LabelRepository(ABC):

    @abstractmethod
    def init_dataset_labels(self, dataset_id: int, file_paths: list[str]):
        pass