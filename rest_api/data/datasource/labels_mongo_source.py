from dataclasses import asdict
from pymongo import MongoClient

from rest_api.domain.models.label_entry import LabelEntry

class LabelsMongoDatasource:
    def __init__(self):
        self.client = MongoClient('mongodb://127.0.0.1:27017')
        self.db = self.client['label_pro']
        self.collection = self.db['labels']
    
    def create_multiple_labels(self, labels: list[LabelEntry]):
        self.collection.insert_many([asdict(e) for e in labels])

    def remove_all_dataset_labels(self, dataset_id: int):
        self.collection = self.db['labels']
        self.collection.delete_many({'dataset_id': int(dataset_id)})

    def find_dataset_labels(self, dataset_id: int):
        dataset_id = int(dataset_id)
        label_entries_db = self.collection.find({'dataset_id': int(dataset_id)})

        label_entries = []
        for e in label_entries_db:
            e : dict
            label_entries.append(LabelEntry.from_dict(e))
        return label_entries
    
    def get_label_entry(self, dataset_id, file_path, id_in_file):
        result = self.collection.find_one({'dataset_id': int(dataset_id), 'file_path': file_path, 'id_in_file': str(id_in_file)})
        print(dataset_id)
        print(file_path)
        print(id_in_file)
        result : dict
        print(result)
        return LabelEntry.from_dict(result)

    
    def update_label_entry(self, label_entry: LabelEntry):
        self.collection.update_one({'dataset_id': label_entry.dataset_id, 'file_path': label_entry.file_path, 'id_in_file': str(label_entry.id_in_file)}, {'$set': asdict(label_entry)})


