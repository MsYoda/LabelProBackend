# Generated by Django 5.2 on 2025-05-09 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0012_dataset_helper_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='folder_path',
            field=models.TextField(default='', max_length=255),
        ),
    ]
