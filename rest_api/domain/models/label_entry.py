from djongo import models

class LabelEntry(models.Model):
    class Meta:
         db_table = "label_entries"