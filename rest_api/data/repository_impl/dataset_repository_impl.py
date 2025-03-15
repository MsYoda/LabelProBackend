
import random
from typing import BinaryIO
from rest_api.domain.models.label_entry import Label, LabelEntry
from rest_api.data.datasource.labels_mongo_source import LabelsMongoDatasource
from rest_api.data.datasource.dataset_db_source import DatasetDBSource
from rest_api.data.datasource.dataset_files_source import DatasetFilesDatasource
from rest_api.domain.repository.dataset_repository import DatasetRepository
from rest_api.domain.models.dataset import Dataset

class DatasetRepositoryImpl(DatasetRepository):
    def __init__(self, files_source, dataset_db_source, labels_mongo_source):
        self.files_source : DatasetFilesDatasource = files_source
        self.dataset_db_source : DatasetDBSource = dataset_db_source
        self.labels_mongo_source : LabelsMongoDatasource = labels_mongo_source

    def create_dataset_files(self, file: BinaryIO, dataset_name: str, folder: str) -> tuple[str, list[str]]:
        return self.files_source.create_dataset_files(file, dataset_name=dataset_name, folder=folder)

    def get_files_count(self, dataset: Dataset) -> int:
        return self.files_source.get_files_count(folder=dataset.folder_path)
    
    def get_dataet_by_id(self, dataset_id: int):
        return self.dataset_db_source.get_by_id(dataset_id)
    
    def get_new_task(self, dataset_id: int, user_id: int):
        dataset = self.dataset_db_source.get_by_id(dataset_id)

        label_entries = self.labels_mongo_source.find_dataset_labels(dataset_id=dataset_id)
        label_entries : list[LabelEntry]

        filtered_entries = []

        for label_entry in label_entries:
            user_tagged = False
            for label in label_entry.labels:
                print(label_entry.file_path)
                if label.status == 'pending':
                    return label_entry
                if label.user_id == user_id:
                    user_tagged = True
                    break
            if not user_tagged:
                filtered_entries.append(label_entry)
        
        result_entry : LabelEntry = random.choice(filtered_entries)
        labels = result_entry.labels
        labels.append(Label(user_id=user_id, status='pending', data={}))

        pending_entry = LabelEntry(id_in_file=result_entry.id_in_file, dataset_id=result_entry.dataset_id, file_path=result_entry.file_path, labels=labels)
        self.labels_mongo_source.update_label_entry(pending_entry)
        
        return result_entry
    
    def submit_task(self, id_in_file: int, dataset_id: int, user_id: int, file_path: str, data: dict):
        label_entry : LabelEntry = self.labels_mongo_source.get_label_entry(id_in_file=id_in_file, dataset_id=dataset_id, file_path=file_path)
        print(label_entry)
        for i, _ in enumerate(label_entry.labels):
            label : Label = label_entry.labels[i]
            if label.status == 'pending' and label.user_id == user_id:
                label_entry.labels[i] = Label(user_id=user_id, status='completed', data=data)
                break
        self.labels_mongo_source.update_label_entry(label_entry=label_entry)
        
    