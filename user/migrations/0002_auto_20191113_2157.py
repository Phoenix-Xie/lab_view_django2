# Generated by Django 2.1.7 on 2019-11-13 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apply',
            name='title',
        ),
        migrations.AlterField(
            model_name='apply',
            name='email',
            field=models.CharField(max_length=20, verbose_name='联系方式'),
        ),
        migrations.AlterField(
            model_name='apply',
            name='name',
            field=models.CharField(default='无', max_length=20, verbose_name='申请人'),
        ),
    ]