from abc import ABC, abstractmethod
import csv


from rest_api.domain.models.label_entry import LabelEntry

class CreateLabelEntryStrategy(ABC):
    @abstractmethod
    def get_entries(self, file_path: str) -> list[LabelEntry]:
        pass

class CreateFromCSV(CreateLabelEntryStrategy):
    def get_entries(self, file_path: str) -> list[LabelEntry]:
        entries = []
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            print(file_path)
            for i, _ in enumerate(reader, start=1):
                entries.append(LabelEntry(id_in_file=str(i), file_path=file_path, dataset_id=1, labels=[]))
        return entries



class CreateFromJSONL(CreateLabelEntryStrategy):
    def get_entries(self, file_path: str) -> list[LabelEntry]:
        entries = []
        with open(file_path, "r", encoding="utf-8") as f:
            for i, _ in enumerate(f, start=1):
                entries.append(LabelEntry(id_in_file=str(i), file_path=file_path, dataset_id=1, labels=[]))
    
class CreateFromTXT(CreateLabelEntryStrategy):
    def get_entries(self, file_path: str) -> list[LabelEntry]:
        entries = []
        with open(file_path, "r", encoding="utf-8") as f:
            for i, _ in enumerate(f, start=1):
                entries.append(LabelEntry(id_in_file=str(i), file_path=file_path, dataset_id=1, labels=[]))
        return entries
    
class CreateFromFile(CreateLabelEntryStrategy):
    def get_entries(self, file_path: str) -> list[LabelEntry]:
        return [LabelEntry(id_in_file='', dataset_id=1, file_path=file_path, labels=[])]

class LabelsCreater:
    def __init__(self, strategy: CreateLabelEntryStrategy):
        self.strategy = strategy

    def process(self, file_path: str):
        return self.strategy.get_entries(file_path)
    

def get_data_reader(file_path: str) -> CreateLabelEntryStrategy:
    extension = file_path.split('.')[-1]
    if extension == 'csv':
        return CreateFromCSV()
    elif extension == 'jsonl':
        return CreateFromJSONL()
    elif extension == 'txt':
        return CreateFromTXT()
    else:
        return CreateFromFile()

