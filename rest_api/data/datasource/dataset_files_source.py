import os
import zipfile
import shutil
from typing import BinaryIO


class DatasetFilesDatasource():
    _basePath = "/Users/user/python/label_pro/datasets/"

    def create_dataset_files(self, file: BinaryIO, dataset_name: str, folder: str) -> tuple[str, list[str]]:
        dataset_name = dataset_name.lower().replace(" ", "_")
        if folder is not None and len(folder) > 0:
            base_folder = folder
        else:
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
                for zip_file in zip_ref.namelist():
                    if zip_file.startswith("__MACOSX/") or os.path.basename(zip_file).startswith("._"):
                        continue
                    zip_ref.extract(zip_file, base_folder)
                    extracted_path = os.path.join(base_folder, zip_file)
                    if os.path.isdir(extracted_path):
                        continue
                    final_path = os.path.join(base_folder, os.path.basename(zip_file))
                    os.rename(extracted_path, final_path)
        else:
            raise TypeError('Provide correct zip arcive please')
        
        
        os.remove(file_path)
        file_paths = []
        for root, dirs, filenames in os.walk(base_folder, topdown=False):
            for file in filenames:
                file_path = os.path.join(root, file)
                file_paths.append(file_path)

            for directory in dirs:
                dir_path = os.path.join(root, directory)
                if not os.listdir(dir_path):
                    shutil.rmtree(dir_path)

        return base_folder, file_paths


    def get_files_count(self, folder: str) -> int:
        try:
            base_folder = folder
            file_count = 0
            for _, __, files in os.walk(base_folder):
                file_count += len(files)
            return file_count
        except FileNotFoundError:
            return 0

