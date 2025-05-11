from abc import ABC, abstractmethod
from datetime import datetime
import json
import os
from PIL import Image
from typing import ChainMap
import zipfile
import xml.etree.ElementTree as ET
from xml.dom import minidom

from django.conf import settings

from rest_api.di.service_locator import ServiceLocator
from rest_api.domain.models.dataset import Dataset, Tag, TaggingTaskType
from rest_api.domain.models.label_entry import Label, LabelEntry
from rest_api.domain.repository.dataset_repository import DatasetRepository

class ExportDatasetStrategy(ABC):
    @abstractmethod
    def export_dataset(self, dataset_id: int, include_source: bool) -> str:
        pass


class JSONLExportProcessor(ExportDatasetStrategy):
    def __init__(self, dataset_repo: DatasetRepository):
        self.dataset_repository = dataset_repo

    def export_dataset(self, dataset_id: int, include_source: bool) -> str:
        dataset: Dataset = self.dataset_repository.get_dataset_by_id(dataset_id)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        temp_dir = os.path.join(settings.BASE_DIR, 'tmp')
        os.makedirs(temp_dir, exist_ok=True)

        filename = f'{dataset.name}_jsonl_{timestamp}.zip'
        file_path = os.path.join(temp_dir, filename)

        with zipfile.ZipFile(file_path, 'w') as zipf:
            with zipf.open('dataset.jsonl', mode='w') as file_in_zip:
                label_entries : list[LabelEntry] = self.dataset_repository.get_dataset_labels(dataset_id)
                for entry in label_entries:
                    data = {}
                    data['file_path'] = os.path.basename(entry.file_path)
                    data['id_in_file'] = entry.id_in_file
                    label: Label | None = entry.labels[0] if entry.labels else None
                    if label is not None:
                        print(label.data)
                        print(type(label.data))
                        test = label.data
                        data = {**data, **test}
                    file_in_zip.write((json.dumps(data, ensure_ascii=False) + '\n').encode('utf-8'))  
        return file_path



class PascalExportProcessor(ExportDatasetStrategy):
    def __init__(self, dataset_repo: DatasetRepository):
        self.dataset_repository = dataset_repo

    def export_dataset(self, dataset_id: int, include_source: bool) -> str:
        dataset: Dataset = self.dataset_repository.get_dataset_by_id(dataset_id)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        tags: list[Tag] = dataset.tags.all()

        temp_dir = os.path.join(settings.BASE_DIR, 'tmp')
        os.makedirs(temp_dir, exist_ok=True)

        filename = f'{dataset.name}_pascalvoc_{timestamp}.zip'
        file_path = os.path.join(temp_dir, filename)

        with zipfile.ZipFile(file_path, 'w') as zipf:
            label_entries : list[LabelEntry] = self.dataset_repository.get_dataset_labels(dataset_id)
            for entry in label_entries:
                abs_path = entry.file_path
                arcname = os.path.join('images', os.path.basename(abs_path))
                zipf.write(abs_path, arcname=arcname)

                filename_wo_ext = os.path.splitext(os.path.basename(abs_path))[0]
                arcname = os.path.join('annotations', filename_wo_ext + '.xml')
                with Image.open(abs_path) as img:
                    img_width, img_height = img.size
                label: Label | None = entry.labels[0] if entry.labels else None

                root = ET.Element("annotation")
                folder = ET.SubElement(root, 'folder')
                folder.text = 'images'

                filename = ET.SubElement(root, 'filename')
                filename.text = os.path.basename(abs_path)

                size = ET.SubElement(root, "size")
                width = ET.SubElement(size, "width")
                width.text = str(img_width)
                height = ET.SubElement(size, "height")
                height.text = str(img_height)

                if label is not None and len(label.data.keys()) > 0:
                    boxes = label.data['boxes']
                    for box_dict in boxes:
                        box = box_dict['box']
                        left = box['left']
                        top = box['top']
                        right = box['right']
                        bottom = box['bottom']

                        label_id = box_dict['label']['id']
                        label_name = None

                        for tag in tags:
                            if label_id == tag.pk:
                                label_name = tag.name
                                break
                        if label_name is not None:
                            obj = ET.SubElement(root, 'object')
                            name = ET.SubElement(obj, 'name')
                            name.text = label_name
                            bndbox = ET.SubElement(obj, 'bndbox')
                            xmin = ET.SubElement(bndbox, 'xmin')
                            xmin.text = str(left)
                            ymin = ET.SubElement(bndbox, 'ymin')
                            ymin.text = str(top)
                            xmax = ET.SubElement(bndbox, 'xmax')
                            xmax.text = str(right)
                            ymax = ET.SubElement(bndbox, 'ymax')
                            ymax.text = str(bottom)

                xml_str = ET.tostring(root, encoding="unicode", method="xml")
                xml_pretty_str = minidom.parseString(xml_str).toprettyxml(indent="  ")
                zipf.writestr(arcname, xml_pretty_str)
        return file_path                 
                  

class YOLOExportProcessor(ExportDatasetStrategy):
    def __init__(self, dataset_repo: DatasetRepository):
        self.dataset_repository = dataset_repo

    def export_dataset(self, dataset_id: int, include_source: bool) -> str:
        dataset: Dataset = self.dataset_repository.get_dataset_by_id(dataset_id)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        tags: list[Tag] = dataset.tags.all()


        temp_dir = os.path.join(settings.BASE_DIR, 'tmp')
        os.makedirs(temp_dir, exist_ok=True)

        filename = f'{dataset.name}_yolo_{timestamp}.zip'
        file_path = os.path.join(temp_dir, filename)

        with zipfile.ZipFile(file_path, 'w') as zipf:
            classes_str = ''
            for tag in tags:
                classes_str += tag.name + '\n'
            zipf.writestr('classess.txt', classes_str)
            
            label_entries : list[LabelEntry] = self.dataset_repository.get_dataset_labels(dataset_id)
            for entry in label_entries:
                abs_path = entry.file_path
                arcname = os.path.join('data', os.path.basename(abs_path))
                zipf.write(abs_path, arcname=arcname)

                filename_wo_ext = os.path.splitext(os.path.basename(abs_path))[0]
                arcname = os.path.join('labels', filename_wo_ext + '.txt')
                with Image.open(abs_path) as img:
                    img_width, img_height = img.size
                label: Label | None = entry.labels[0] if entry.labels else None
                label_str = ''
                if label is not None and len(label.data.keys()) > 0:
                    boxes = label.data['boxes']
                    for box_dict in boxes:
                        box = box_dict['box']
                        left = box['left']
                        top = box['top']
                        right = box['right']
                        bottom = box['bottom']

                        center_x = (left + right) / 2
                        center_y = (top + bottom) / 2
                        width = abs(right - left)
                        height = abs(top - bottom)

                        label_id = box_dict['label']['id']
                        label_index = None

                        for i, tag in enumerate(tags):
                            if tag.pk == label_id:
                                label_index = i
                                break
                        if label_index != None:
                            label_str += f'{label_index} {center_x / img_width} {center_y / img_height} {width / img_width} {height / img_height}'
                zipf.writestr(arcname, label_str)
        return file_path



class COCOExportProcessor(ExportDatasetStrategy):
    def __init__(self, dataset_repo: DatasetRepository):
        self.dataset_repository = dataset_repo

    def export_dataset(self, dataset_id: int, include_source: bool) -> str:
        dataset: Dataset = self.dataset_repository.get_dataset_by_id(dataset_id)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        tags: list[Tag] = dataset.tags.all()

        temp_dir = os.path.join(settings.BASE_DIR, 'tmp')
        os.makedirs(temp_dir, exist_ok=True)

        filename = f'{dataset.name}_coco_{timestamp}.zip'
        file_path = os.path.join(temp_dir, filename)

        with zipfile.ZipFile(file_path, 'w') as zipf:
            label_entries : list[LabelEntry] = self.dataset_repository.get_dataset_labels(dataset_id)
            dataset_dict = {}
            dataset_dict['categories'] = []
            dataset_dict['annotations'] = []
            dataset_dict['images'] = []
            for i, tag in enumerate(tags):
                dataset_dict['categories'].append({
                    'id': i,
                    'name': tag.name,
                })
                
            for i, entry in enumerate(label_entries):
                abs_path = entry.file_path
                zipf.write(abs_path, arcname=os.path.basename(abs_path))
                with Image.open(abs_path) as img:
                    img_width, img_height = img.size
                dataset_dict['images'].append({
                    'image_id': i,
                    'file_name': os.path.basename(abs_path),
                    'width': img_width,
                    'height': img_height,
                })

                label: Label | None = entry.labels[0] if entry.labels else None
                if label is not None and len(label.data.keys()) > 0:
                    if dataset.type == TaggingTaskType.bounding_box:
                        boxes = label.data['boxes']
                        for box_dict in boxes:
                            annotation = {}

                            box = box_dict['box']
                            left = box['left']
                            top = box['top']
                            right = box['right']
                            bottom = box['bottom']

                            width = abs(right - left)
                            height = abs(top - bottom)

                            label_id = box_dict['label']['id']
                            label_index = None

                            for tag_index, tag in enumerate(tags):
                                if tag.pk == label_id:
                                    label_index = tag_index
                                    break

                            if label_index is not None:
                                annotation['image_id'] = i
                                annotation['category_id'] = label_index
                                annotation['bbox'] = [left, top, width, height]
                                dataset_dict['annotations'].append(annotation)
                            
                    elif dataset.type == TaggingTaskType.polygons:
                        polygons = label.data['polygons']
                        for poly_dict in polygons:
                            annotation = {}
                            points_dicts = poly_dict['points']
                            points = []
                            for point_dict in points_dicts:
                                points.append(point_dict['x'])
                                points.append(point_dict['y'])

                            label_id = poly_dict['label']['id']
                            label_index = None

                            for tag_index, tag in enumerate(tags):
                                if tag.pk == label_id:
                                    label_index = tag_index
                                    break

                            if label_index is not None:
                                annotation['image_id'] = i
                                annotation['category_id'] = label_index
                                annotation['poly'] = points
                                dataset_dict['annotations'].append(annotation)
            zipf.writestr('dataset.json', json.dumps(dataset_dict,indent=4, ensure_ascii=False))
        return file_path

class ExportProcessor():
    def __init__(self, strategy: ExportDatasetStrategy):
        self.strategy = strategy

    def export_dataset(self, dataset_id: int, include_source: bool):
        return self.strategy.export_dataset(dataset_id, include_source=include_source)
    
    @staticmethod
    def get_exporter(export_format: str) -> ExportDatasetStrategy:
        dataset_repo = ServiceLocator.get(DatasetRepository)

        if export_format == 'yolo':
            return YOLOExportProcessor(dataset_repo)
        elif export_format == 'coco':
            return COCOExportProcessor(dataset_repo)
        elif export_format == 'pascalvoc':
            return PascalExportProcessor(dataset_repo)
        else:
            return JSONLExportProcessor(dataset_repo)
    
