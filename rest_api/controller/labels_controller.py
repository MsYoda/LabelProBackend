from django.http import FileResponse, HttpResponse
from rest_framework.views import APIView

from rest_api.domain.repository.dataset_repository import DatasetRepository
from rest_api.di.service_locator import ServiceLocator

class LabelsController(APIView):
    dataset_repository : DatasetRepository = ServiceLocator.get(DatasetRepository)
    def get(self, request):
        dataset_id = request.query_params.get("dataset_id", 1)
        print(dataset_id)
        label_entry = self.dataset_repository.get_new_task(dataset_id=dataset_id, user_id=1)
        # implement metadata fetching
        return HttpResponse({'data': 'data', 'metadata': ''})
