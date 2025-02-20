from django.contrib import admin

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


class DatasetAdmin(admin.ModelAdmin):
    form = DatasetAdminForm
    list_display = ('name',)
    readonly_fields = ('files_count',)
    search_fields = ['name'] 
    inlines = [TagInline]

    def files_count(self, obj):
        dataset_repo: DatasetRepository = ServiceLocator.get(DatasetRepository)
        return dataset_repo.get_files_count(obj.name)
    
    files_count.short_description = 'Files count'

    fieldsets = (
        (None, {
            'fields': ('name', 'files')
        }),
        ('Dataset Info', {
            'fields': ('files_count',),
        }),
    )

    def save_model(self, request, obj, form, change):
        uploaded_file = form.cleaned_data.get('files')
        dataset_repo: DatasetRepository = ServiceLocator.get(DatasetRepository)

        if uploaded_file:
            dataset_repo.create_dataset_files(uploaded_file, form.cleaned_data.get('name'))

        super().save_model(request, obj, form, change)


admin.site.register(Dataset, DatasetAdmin)
admin.site.register(Tag, TagAdmin)