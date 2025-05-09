from django.contrib import admin
from django.contrib import messages

from rest_api.domain.repository.label_repository import LabelRepository
from rest_api.di.service_locator import ServiceLocator
from rest_api.domain.repository.dataset_repository import DatasetRepository
from rest_api.forms import DatasetAdminForm

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


@admin.action(description='Export dataset')
def custom_action(modeladmin, request, queryset):
    for obj in queryset:
        pass
    messages.success(request, "Действие выполнено!")

class DatasetAdmin(admin.ModelAdmin):
    change_form_template = "dataset_change_form.html"
    form = DatasetAdminForm
    list_display = ('name',)
    readonly_fields = ('files_count', 'id')
    search_fields = ['name'] 
    inlines = [TagInline]
    actions = [custom_action]

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