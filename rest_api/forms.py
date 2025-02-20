from django import forms
from django.core.validators import FileExtensionValidator

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
