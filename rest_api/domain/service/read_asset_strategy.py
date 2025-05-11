from abc import ABC, abstractmethod
import csv
import json

class ReadAssetStrategy(ABC):
    @abstractmethod
    def get_data(self, file_name: str, id_in_file: str, data_key):
        pass

class CSVDataReader(ReadAssetStrategy):
    def get_data(self, file_name: str, id_in_file: str, data_key):
        with open(file_name, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for current_line, row in enumerate(reader, start=1):
                if current_line == int(id_in_file):
                    return row[data_key]

class JSONDataReader(ReadAssetStrategy):
    def get_data(self, file_name: str, id_in_file: str, data_key):
        with open(file_name, 'r', encoding='utf-8') as f:
            for current_line, line in enumerate(f, start=1):
                if current_line == int(id_in_file):
                    json_data = json.loads(line.strip())
                    return json_data.get(data_key, None)
        return None
    
class TXTDataReader(ReadAssetStrategy):
    def get_data(self, file_name: str, id_in_file: str, data_key=None):
        with open(file_name, 'r', encoding='utf-8') as f:
            for current_line, line in enumerate(f, start=1):
                if current_line == int(id_in_file):
                    return line.strip()
        return None
    
class FileDataReader(ReadAssetStrategy):
    def get_data(self, file_name: str, id_in_file: str, data_key):
        return file_name

class AssetReader:
    def __init__(self, strategy: ReadAssetStrategy):
        self.strategy = strategy

    def read(self, file_name: str, id_in_file: str, data_key):
        return self.strategy.get_data(file_name, id_in_file, data_key)
    
    @staticmethod
    def get_data_reader(file_name: str) -> ReadAssetStrategy:
        extension = file_name.split('.')[-1]
        if extension == 'csv':
            return CSVDataReader()
        elif extension == 'jsonl':
            return JSONDataReader()
        elif extension == 'txt':
            return TXTDataReader()
        else:
            return FileDataReader()

