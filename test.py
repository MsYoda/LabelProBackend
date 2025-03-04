from dataclasses import asdict
import pymongo

from rest_api.domain.service.read_asset_strategy import AssetReader
from rest_api.domain.service.create_label_entry_strategy import LabelsCreater, get_data_reader
from rest_api.domain.models.label_entry import LabelEntry

client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client['label_pro']
collection = db['labels']

label_entries = collection.find()
file_path = '/Users/user/python/label_pro/datasets/hello_bro/20.png'


strategy = AssetReader.get_data_reader('./test.svg')
labels_creater : AssetReader = AssetReader(strategy)
r = labels_creater.read('./test.svg', id_in_file=3, data_key='name')
print(r)
# for v in label_entries:
#     print(v)


# collection.update_one({'dataset_id': 1, 'file_path': file_path}, {'$set': asdict(LabelEntry(dataset_id=1, file_path=file_path, file_part=1 ,labels=[]))})

# collection.delete_many({})

# for v in label_entries:
#     v:dict
#     print(v)
#     v.pop('_id')
#     print(LabelEntry(**v))

# client.close()
# print('finish')