# Generated by Django 4.2.12 on 2025-02-24 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0004_dataset_folder_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='min_labels_for_file',
            field=models.IntegerField(default=1),
        ),
    ]
