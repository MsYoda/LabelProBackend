from django import forms
from django.core.validators import FileExtensionValidator
from django_admin_action_forms import AdminActionFormsMixin, AdminActionForm, action_with_form

from rest_api.domain.models.dataset import TaggingTaskType

from .models import Dataset


class DatasetAdminForm(forms.ModelForm):
    files = forms.FileField(
        label="Replace files with .zip",
        required=False,
        validators=[FileExtensionValidator(allowed_extensions=['zip'], message='Use .zip')],
        widget=forms.FileInput(),
    )

    class Meta:
        model = Dataset
        fields = '__all__'


class ExportDatasetForm(AdminActionForm):
    FORMAT_CHOICES = [
        ('yolo', 'YOLO'),
        ('jsonl', 'JSONL'),
        ('pascalvoc', 'PascalVOC'),
        ('coco', 'COCO'),
    ]
    INCLUDE_SOURCE_CHOISES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    format = forms.ChoiceField(
        choices=FORMAT_CHOICES,
        label="Export format",
        required=True
    )

    include_source_files= forms.ChoiceField(
        choices=INCLUDE_SOURCE_CHOISES,
        label="Include source files",
        required=True,
        initial='no',
    )

    class Meta:
        list_objects = True
        help_text = "Are you sure that you want to export dataset?"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dataset : Dataset = self.queryset.first()
        if dataset.type == TaggingTaskType.bounding_box:   
            self.fields['format'].choices = self.FORMAT_CHOICES
        elif dataset.type == TaggingTaskType.polygons:
            self.fields['format'].choices = [ ('coco', 'COCO'), ('jsonl', 'JSONL'),]
        else:
            self.fields['format'].choices = [ ('jsonl', 'JSONL'),]