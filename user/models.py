from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


# Create your models here.


class Instrument(models.Model):
    # id = models.IntegerField("id", "id", True, 100000, True, False, False)
    number = models.CharField(verbose_name="编号", max_length=100, default='')
    name = models.CharField(verbose_name="仪器名称", max_length=500)
    model_number = models.CharField(verbose_name="仪器编号", max_length=500)
    maker = models.CharField(verbose_name="厂家", max_length=500)
    type = models.CharField(verbose_name="类别", max_length=500)
    lab_id = models.ForeignKey('Lab', verbose_name="所属实验室", on_delete=models.CASCADE)
    is_lend = models.BooleanField(verbose_name='是否出借', default=False)

    class Meta:
        verbose_name = r'实验仪器'
        verbose_name_plural = r'实验仪器'
        get_latest_by = 'number'

    def __str__(self):
        return self.name


class Lab(models.Model):
    # id = models.IntegerField("id", "id", True, 100000, True, False, False)
    department_id = models.ForeignKey('Department', on_delete=models.CASCADE, verbose_name="关联学院")
    name = models.CharField(verbose_name="实验室名称", max_length=500)

    class Meta:
        verbose_name = r'实验室'
        verbose_name_plural = r'实验室'

    def __str__(self):
        return self.name


class Department(models.Model):
    # id = models.IntegerField("id", "id", True, 100000, True, False, False)
    name = models.CharField(verbose_name="学院名称", max_length=100)

    class Meta:
        verbose_name = '学院'
        verbose_name_plural = '学院'

    def __str__(self):
        return self.name


class ApplyInstrumentList(models.Model):
    Instrument_id = models.ForeignKey('Instrument', verbose_name="仪器", on_delete=models.CASCADE)
    Apply_id = models.ForeignKey('Apply', verbose_name="申请", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '申请对应仪器表'
        verbose_name = '申请对应仪器表'

    def __str__(self):
        return "对应关系" + str(self.id)


class Apply(models.Model):
    # ApplyInstrumentList_id = models.ForeignKey('ApplyInstrumentList', verbose_name="申请", on_delete=models.CASCADE)
    email = models.CharField(verbose_name='邮箱', max_length=20)
    weid = models.CharField(verbose_name="微信id", max_length=30, default='')
    title = models.CharField(verbose_name="标题", max_length=100)
    text = models.TextField(verbose_name="内容", max_length=1000)
    time = models.DateField(verbose_name='申请时间')
    statu = models.SmallIntegerField(choices=[(1, "通过"), (-1, "未通过"), (0, "未处理"), (2, "已归还")], verbose_name="状态", default=0)
    name = models.CharField(verbose_name="申请人姓名", default="无", max_length=10)
    openId = models.CharField(max_length=32, verbose_name="用户微信的openId", default="None")
    formId = models.CharField(verbose_name="表单id", default="无", max_length=50)


    class Meta:
        verbose_name_plural = '申请'
        verbose_name = '申请'
        permissions = (
            ('view_task', '查看权限'),
            ('change_task', '修改权限')
        )

    def __str__(self):
        return self.title


class MyUser(AbstractUser):
    belong_lab = models.ManyToManyField(Lab,verbose_name="所属实验室",related_name="belongLab",blank=True,null=True)