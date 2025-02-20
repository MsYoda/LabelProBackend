import os
import zipfile
import shutil
from typing import BinaryIO


class DatasetFilesDatasource():
    _basePath = "/Users/user/python/label_pro/datasets/"

    def create_dataset_files(self, file: BinaryIO, dataset_name: str) -> None:
        dataset_name = dataset_name.lower().replace(" ", "_")
        base_folder = f"{self._basePath}{dataset_name}"

        if os.path.exists(base_folder):
            shutil.rmtree(base_folder)

        os.makedirs(os.path.dirname(base_folder), exist_ok=True)
        file_path = base_folder + file.name

        with open(file_path, "wb") as dest:
            for chunk in file.chunks():
                dest.write(chunk)

        if zipfile.is_zipfile(file_path):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(base_folder)
        else:
            raise TypeError('Provide correct zip arcive please')
        os.remove(file_path)

    def get_files_count(self, dataset_name: str) -> int:
        try:
            dataset_name = dataset_name.lower().replace(" ", "_")
            base_folder = f"{self._basePath}{dataset_name}"
            file_count = 0
            for _, __, files in os.walk(base_folder):
                file_count += len(files)
            return file_count
        except FileNotFoundError:
            return 0
