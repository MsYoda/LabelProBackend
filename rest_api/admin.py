import os
from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib import messages
from django.http import FileResponse, HttpResponse
from django_admin_action_forms import AdminActionFormsMixin, AdminActionForm, action_with_form

from rest_api.domain.repository.label_repository import LabelRepository
from rest_api.di.service_locator import ServiceLocator
from rest_api.domain.repository.dataset_repository import DatasetRepository
from rest_api.domain.service.export_dataset_strategy import ExportProcessor
from rest_api.forms import DatasetAdminForm, ExportDatasetForm

from .domain.models.dataset import Dataset, Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'class_id', 'dataset') 
    search_fields = ['name']
    list_filter = ('dataset',)

    readonly_fields = ('class_id',)


class TagInline(admin.TabularInline):
    model = Tag
    fields = ['name']
    show_change_link = True
    actions = ['delete_selected']
    extra = 0

@action_with_form(
    ExportDatasetForm,
    description="Export dataset",
)
def export_action(self, request, queryset, data):
    format = data['format']
    include_source_files = data['include_source_files'] == 'yes'

    if len(queryset) > 1:
        messages.error(request, 'You cant use this action with more than one dataset')
        return
    
    obj: Dataset = queryset.first()

    archive_path = ExportProcessor(ExportProcessor.get_exporter(format)).export_dataset(obj.pk, include_source_files)

    stream_file = open(archive_path, 'rb')
    original_close = stream_file.close

    def new_close():
        original_close()
        os.remove(stream_file.name)

    stream_file.close = new_close

    return FileResponse(stream_file, as_attachment=True)


class DatasetAdmin(AdminActionFormsMixin, admin.ModelAdmin):
    change_form_template = "dataset_change_form.html"
    form = DatasetAdminForm
    list_display = ('name',)
    readonly_fields = ('files_count', 'id')
    search_fields = ['name'] 
    inlines = [TagInline]
    actions = [export_action]


    def files_count(self, obj):
        dataset_repo: DatasetRepository = ServiceLocator.get(DatasetRepository)
    
        return dataset_repo.get_files_count(obj)
    
    files_count.short_description = 'Files count'


    fieldsets = (
        (None, {
            'fields': ('name', 'folder_path', 'min_labels_for_file','helper_text', 'data_key', 'files',)
        }),
        ('Labeling configuration', {
            'fields': ('type', 'input_type', 'data_type'),
            'classes': ('collapse',),
        }),
        ('Dataset Info', {
            'fields': ('id', 'files_count',),
        }),
    )

    def save_model(self, request, obj, form, change):
        uploaded_file = form.cleaned_data.get('files')
        dataset_repo: DatasetRepository = ServiceLocator.get(DatasetRepository)
        label_repo: LabelRepository = ServiceLocator.get(LabelRepository)

        if uploaded_file:
            folder, file_paths = dataset_repo.create_dataset_files(uploaded_file, form.cleaned_data.get('name'), obj.folder_path)
            obj.folder_path = folder
        
        super().save_model(request, obj, form, change)

        if uploaded_file:
            label_repo.init_dataset_labels(dataset_id=obj.pk, file_paths=file_paths)


admin.site.register(Dataset, DatasetAdmin)
admin.site.register(Tag, TagAdmin)