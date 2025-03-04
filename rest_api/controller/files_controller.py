from django.http import FileResponse
from rest_framework.views import APIView

from rest_api.domain.repository.dataset_repository import DatasetRepository

class FilesController(APIView):
    def get(self, request):
        file_path = request.query_params.get("file_path", "")

        return FileResponse(open(file_path, 'rb'))
