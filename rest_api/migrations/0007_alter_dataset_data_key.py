# Generated by Django 4.2.12 on 2025-02-26 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0006_dataset_data_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='data_key',
            field=models.TextField(default='', max_length=255),
        ),
    ]
