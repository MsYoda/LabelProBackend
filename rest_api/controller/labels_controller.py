from django.http import FileResponse, HttpResponse, JsonResponse
from rest_framework.views import APIView

from rest_api.domain.models.dataset import Dataset
from rest_api.domain.models.label_entry import LabelEntry
from rest_api.domain.service.read_asset_strategy import AssetReader
from rest_api.domain.repository.dataset_repository import DatasetRepository
from rest_api.di.service_locator import ServiceLocator

class LabelsController(APIView):
    dataset_repository : DatasetRepository = ServiceLocator.get(DatasetRepository)
    def get(self, request):
        dataset_id = request.query_params.get("dataset_id", 1)
        print(dataset_id)
        label_entry : LabelEntry = self.dataset_repository.get_new_task(dataset_id=dataset_id, user_id=1)
        dataset : Dataset = self.dataset_repository.get_dataet_by_id(dataset_id)
        asset_reader : AssetReader = AssetReader(AssetReader.get_data_reader(label_entry.file_path))
        
        return JsonResponse({'data': asset_reader.read(label_entry.file_path, 
                                                       id_in_file=label_entry.id_in_file, 
                                                       data_key=dataset.data_key), 'metadata': ''})
    def post(self, request):
        id_in_file= request.data.get('id_in_file')
        file_path = request.data.get('file_path')
        dataset_id = request.data.get('dataset_id')
        data = request.data.get('data')
        user_id = request.data.get('user_id')
        self.dataset_repository.submit_task(id_in_file=id_in_file,
                                            user_id=user_id,
                                            file_path=file_path,
                                            dataset_id=dataset_id,
                                            data=data)
        return HttpResponse()
