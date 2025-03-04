from rest_api.domain.service.create_label_entry_strategy import get_data_reader, LabelsCreater
from rest_api.data.datasource.labels_mongo_source import LabelsMongoDatasource
from rest_api.domain.models.label_entry import LabelEntry
from rest_api.domain.repository.label_repository import LabelRepository



class LabelRepositoryImpl(LabelRepository):
    def __init__(self, mongo_source : LabelsMongoDatasource):
        self.labels_mongo_source = mongo_source
       

    def init_dataset_labels(self, dataset_id: int, file_paths: list[str]):
        labels = []
        print('paths')
        print(file_paths)
        for file in file_paths:
            strategy = get_data_reader(file)
            labels_creater : LabelsCreater = LabelsCreater(strategy)
            result : list[LabelEntry] = labels_creater.process(file_path=file)
            full_result = [LabelEntry(dataset_id=dataset_id, file_path=e.file_path, id_in_file=e.id_in_file, labels=[]) for e in result]
            labels.extend(full_result)
            
        self.labels_mongo_source.remove_all_dataset_labels(dataset_id=dataset_id)
        self.labels_mongo_source.create_multiple_labels(labels=labels)

        

        