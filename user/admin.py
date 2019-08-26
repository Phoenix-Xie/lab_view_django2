from django.contrib import admin, messages
from django.contrib.admin.actions import delete_selected
# xie  123456
# Register your models here.
from user.tools import pushMsgThread
from .models import Instrument, Lab, Department, ApplyInstrumentList, Apply, MyUser

# from guardian.admin import GuardedModelAdmin

delete_selected.short_description = "删除所有所选项"


class ApplyInstrumentListInline(admin.StackedInline):
    model = ApplyInstrumentList
    extra = 3
    readonly_fields = ('Instrument_id', )

    def get_readonly_fields(self, request, obj=None):
        """  重新定义此函数，限制普通用户所能修改的字段  """
        if request.user.is_superuser:
            self.readonly_fields = []
        return self.readonly_fields


# @admin.register(Apply)
class ApplyAdmin(admin.ModelAdmin):
    inlines = [ApplyInstrumentListInline]
    list_display = ('title', 'time',  'name', 'statu')
    ordering = ('-time',)
    actions = [
        'pass_apply',
        'not_pass_apply',
    ]

    search_fields = ['title']

    def pass_apply(self, request, queryset):
        for apply in queryset:
            if apply.statu != 0:
                messages.warning(request, "标题:{} 的申请已处理过".format(apply.title))
                continue

            email = apply.email
            apply_instrument_list = ApplyInstrumentList.objects.filter(Apply_id=apply)
            flag = True
            for ai in apply_instrument_list:
                if ai.Instrument_id.is_lend:
                    flag = False
                    break
            if not flag:
                messages.error(request, "操作失败，编号为{}的{}已借出".format(str(ai.Instrument_id.number), ai.Instrument_id.name))
            else:
                goods_names=""
                for ai in apply_instrument_list:
                    ai.Instrument_id.is_lend = True
                    ai.Instrument_id.save()
                    goods_names=goods_names+ai.Instrument_id.name +" "
                apply.statu = 1
                pushThread = pushMsgThread(apply.formId, apply.openId, apply.name, "预约成功", goods_names)
                pushThread.start()
                apply.save()
                self.message_user(request, "成功通过申请")

    pass_apply.short_description = "通过选定申请"

    def not_pass_apply(self, request, queryset):
        for apply in queryset:
            email = apply.email
            if apply.statu == 0:
                apply.statu = -1
                apply.save()
                self.message_user(request, "成功拒绝申请")
                pushThread = pushMsgThread(apply.formId, apply.openId, apply.name, "预约失败", "预约失败")
                pushThread.start()
                apply.save()
            else:
                messages.error(request, "该申请已处理过")

    not_pass_apply.short_description = "拒绝选定申请"

    readonly_fields = ('id', 'title', 'text', 'time', 'name')

    def get_readonly_fields(self, request, obj=None):
        """  重新定义此函数，限制普通用户所能修改的字段  """
        if request.user.is_superuser:
            self.readonly_fields = []
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        # 超级管理员的肆无忌惮

        if request.user.is_superuser:
            super().save_model(request, obj, form, change)
        # 普通用户的无奈选择
        else:
            if obj.statu != 0:
                messages.error(request, "该申请已处理")
            else:
                super().save_model(request, obj, form, change)


# @admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    actions = [
        'set_is_lend',
        'set_not_lend',
    ]
    list_display = ('name', 'type', 'maker', 'is_lend')
    ordering = ('id',)

    search_fields = ['name']

    def set_is_lend(self, request, queryset):
        if request.user.belong_lab!=queryset[0].lab_id:
            print(("无权"))
        else:
            for ins in queryset:
                ins.is_lend = True
                ins.save()
            self.message_user(request, "已全部设置为借出")

    def set_not_lend(self, request, queryset):
        if request.user.belong_lab!=queryset[0].lab_id:
            print(("无权"))
        else:
            for ins in queryset:
                ins.is_lend = False
                ins.save()
            self.message_user(request, "已全部设置为未借出")


class LabAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    ordering = ('id',)

    search_fields = ['name']


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    ordering = ('id',)

    search_fields = ['name']


admin.site.register(Apply, ApplyAdmin)
admin.site.register(Instrument, InstrumentAdmin)
admin.site.register(Lab, LabAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(ApplyInstrumentList)

admin.site.register(MyUser)