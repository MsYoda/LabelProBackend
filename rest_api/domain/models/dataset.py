from django.db import models

class TaggingTaskType(models.TextChoices):
    bounding_box = 'bounding_box', 
    polygons = 'polygons',
    word_tagging = 'word_tagging',
    custom = 'custom',


class CustomInputType(models.TextChoices):
    text = 'text',
    one_from_many = 'one_from_many',
    many_from_many = 'many_from_many'

class CustomDataType(models.TextChoices):
    sound = 'sound',
    image = 'image',
    string = 'string'


class Dataset(models.Model):
    name = models.CharField(max_length=255)
    id = models.AutoField(primary_key=True, editable=False)
    folder_path = models.CharField(default='', max_length=1024, blank=True)
    min_labels_for_file = models.IntegerField(default=1)
    data_key = models.CharField(default='', max_length=255, blank=True)
    helper_text = models.CharField(default='', blank=True)

    type = models.CharField(
        max_length=50,
        choices=TaggingTaskType.choices,
        default=TaggingTaskType.choices[0]
    )

    input_type = models.CharField(
        max_length=50,
        choices=CustomInputType.choices,
        default='',
        blank=True,
        null=True,
    )

    data_type = models.CharField(
        max_length=50,
        choices=CustomDataType.choices,
        default='',
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = "datasets"


class Tag(models.Model):
    name = models.CharField(max_length=50, blank=False)
    id = models.AutoField(primary_key=True, editable=False)
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

