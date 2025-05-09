from django.http import FileResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from rest_api.domain.models.dataset import Dataset, Tag
from rest_api.di.service_locator import ServiceLocator
from rest_api.domain.repository.dataset_repository import DatasetRepository

class DatasetController(APIView):
    permission_classes = [IsAuthenticated]

    dataset_repository : DatasetRepository = ServiceLocator.get(DatasetRepository)

    def get(self, request, dataset_id: int):
        dataset: Dataset = self.dataset_repository.get_dataet_by_id(dataset_id=dataset_id)
        tags: list[Tag] = Tag.objects.filter(dataset=dataset)
        return JsonResponse({
            'id': dataset.id,
            'name': dataset.name,
            'tasksType': dataset.type, 
            'helperText': dataset.helper_text,           
            'availableLabels': [{'id': e.id, 'name': e.name} for e in tags],
        })
