# Generated by Django 2.1.7 on 2019-10-29 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20191029_2318'),
        ('excelmodule', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='excelimporter',
            name='lab_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='user.Lab', verbose_name='所属实验室'),
            preserve_default=False,
        ),
    ]
