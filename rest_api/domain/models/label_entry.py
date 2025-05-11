import json
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Label:
    user_id: int
    status: str
    data: dict

    def __post_init__(self):
        if isinstance(self.data, str):
            self.data = json.loads(self.data)

@dataclass
class LabelEntry:
    dataset_id: int
    file_path: str
    id_in_file: str
    labels: List[Label]

    @staticmethod
    def from_dict(data: Dict):
        labels = [Label(**label) for label in data['labels']]
        return LabelEntry(
            dataset_id=data['dataset_id'],
            file_path=data['file_path'],
            id_in_file=data['id_in_file'],
            labels=labels
        )
          
    