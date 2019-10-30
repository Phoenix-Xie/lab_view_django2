from django.db import models
from user.models import Lab
# Create your models here.


class ExcelImporter(models.Model):
    excel_file = models.FileField(upload_to="excel/%Y/%m/%d/")
    lab_id = models.ForeignKey(Lab, verbose_name="所属实验室", on_delete=models.CASCADE)

    def __str__(self):
        return self.excel_file.name

    class Meta:
        verbose_name = r'导入Excel'
        verbose_name_plural = r'导入Excel'