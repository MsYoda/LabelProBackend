import uuid
from django.db import models

class Dataset(models.Model):
    name = models.CharField(max_length=255)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = "datasets"


class Tag(models.Model):
    name = models.CharField(max_length=50, blank=False)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    class_id = models.IntegerField()
    dataset = models.ForeignKey(Dataset, related_name='tags', on_delete=models.CASCADE)


    def save(self, *args, **kwargs):
        if not self.class_id:
            last_class_id = Tag.objects.filter(dataset=self.dataset).aggregate(models.Max('class_id'))['class_id__max']
            self.class_id = (last_class_id or 0) + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = "tags"

