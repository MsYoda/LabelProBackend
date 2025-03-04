from rest_api.domain.models.dataset import Dataset


class DatasetDBSource:

    def get_by_id(self, dataset_id : int) -> Dataset:
        result = Dataset.objects.filter(id=dataset_id).first()
        return result
