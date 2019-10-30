from django.contrib import admin, messages
from django.contrib.admin.actions import delete_selected
# xie  123456
# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import UserManager

from user.tools import pushMsgThread, sendEmailThread
from .models import Instrument, Lab, Department, ApplyInstrumentList, Apply, MyUser
import xlrd

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
        "deal_end_apply",
    ]

    search_fields = ['title']

    def pass_apply(self, request, queryset):
        current_user = request.user
        for apply in queryset:
            if apply.statu != 0:
                messages.warning(request, "标题:{} 的申请已处理过".format(apply.title))
                continue


            apply_instrument_list = ApplyInstrumentList.objects.filter(Apply_id=apply)
            flag = True
            is_allow=True
            for ai in apply_instrument_list:
                if ai.Instrument_id.is_lend:
                    messages.error(request,
                                   "操作失败，编号为{}的{}已借出".format(str(ai.Instrument_id.number), ai.Instrument_id.name))
                    flag = False
                    break
                else:
                    if not current_user.is_superuser:
                        if ai.Instrument_id.lab_id not in current_user.belong_lab.all():
                            messages.error(request, "操作失败，您没有权限操作名字为{}的实验室申请".format(str(ai.Instrument_id.lab_id.name)))
                            is_allow=False
                            break
            if not flag or not is_allow:
                # messages.error(request, "操作失败，编号为{}的{}已借出".format(str(ai.Instrument_id.number), ai.Instrument_id.name))
                pass
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
                email = apply.email
                content="用户:"+apply.name+", 您申请的:"+goods_names+",已经通过申请审核."
                sendMail = sendEmailThread("实验室管理系统", content, email)
                sendMail.start()
                self.message_user(request, "成功通过{}的申请".format(apply.name))

    pass_apply.short_description = "通过选定申请"

    def not_pass_apply(self, request, queryset):
        current_user = request.user
        for apply in queryset:
            if not current_user.is_superuser:
                goods=ApplyInstrumentList.objects.filter(Apply_id=apply)[0]
                if goods.Instrument_id.lab_id not in current_user.belong_lab.all():
                    messages.error(request, "操作失败，您没有权限操作名字为{}的实验室申请".format(str(goods.Instrument_id.lab_id.name)))
                    return

            email = apply.email
            if apply.statu == 0:
                apply.statu = -1
                apply.save()
                self.message_user(request, "成功拒绝申请")
                pushThread = pushMsgThread(apply.formId, apply.openId, apply.name, "预约失败", "预约失败")
                pushThread.start()
                email = apply.email
                content = "用户:" + apply.name + ", 您申请的实验室设备,未通过申请审核."
                sendMail = sendEmailThread("实验室管理系统", content, email)
                sendMail.start()

                apply.save()
            else:
                messages.error(request, "该申请已处理过")

    not_pass_apply.short_description = "拒绝选定申请"

    def deal_end_apply(self, request, queryset):
        current_user = request.user
        for apply in queryset:
            if not current_user.is_superuser:
                goods=ApplyInstrumentList.objects.filter(Apply_id=apply)[0]
                if goods.Instrument_id.lab_id not in current_user.belong_lab.all():
                    messages.error(request, "操作失败，您没有权限操作名字为{}的实验室申请".format(str(goods.Instrument_id.lab_id)))
                    return
            if apply.statu == 1:
                apply.statu = 2
                apply.save()
                apply_instrument_list = ApplyInstrumentList.objects.filter(Apply_id=apply)
                for ai in apply_instrument_list:
                    if ai.Instrument_id.is_lend:
                        ai.Instrument_id.is_lend = False
                self.message_user(request, "成功完结该申请并归还设备")
                apply.save()
            else:
                messages.error(request, "该申请尚未被处理过")

    deal_end_apply.short_description = "完结并归还选定申请"

    readonly_fields = ('id', 'title', 'text', 'time', 'name')

    def get_readonly_fields(self, request, obj=None):
        """  重新定义此函数，限制普通用户所能修改的字段  """
        if request.user.is_superuser:
            self.readonly_fields = []
        return self.readonly_fields

    def save_model(self, request, obj, form, change):


        if request.user.is_superuser:
            super().save_model(request, obj, form, change)
        # 普通用户的无奈选择
        else:
            goods = ApplyInstrumentList.objects.filter(Apply_id=obj)[0]
            if goods.Instrument_id.lab_id not in request.user.belong_lab.all():
                messages.error(request, "操作失败，您不能操作其他实验室的设备")
                return

            if obj.statu != 0:
                messages.error(request, "该申请已处理")
            else:
                super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        if request.user.is_superuser:
            super().delete_model(request, obj)
        # 普通用户的无奈选择
        else:
            goods = ApplyInstrumentList.objects.filter(Apply_id=obj)[0]
            if goods.Instrument_id.lab_id not in request.user.belong_lab.all():
                messages.error(request, "操作失败，您不能操作其他实验室的设备")
                return
            else:
                super().delete_model(request, obj)

# @admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    actions = [
        'set_is_lend',
        'set_not_lend',
        "deleteSelected",
    ]
    list_display = ('name', 'type', 'maker',"lab_id", 'is_lend')
    ordering = ('id',)
    list_filter = ['lab_id', "type"]

    search_fields = ['name']
    admin.site.disable_action('delete_selected')  # 禁用删除

    def deleteSelected(modeladmin, request, queryset):
        for one in queryset:
            if one.lab_id not in request.user.belong_lab.all() and not request.user.is_superuser:
                messages.error(request, "操作{}失败，您不能操作其他实验室的设备".format(one.name))
            else:
                one.delete()

    deleteSelected.short_description = "删除指定内容"

    def save_model(self, request, obj, form, change):
        if obj.lab_id not in request.user.belong_lab.all() and not request.user.is_superuser:
            messages.error(request, "操作失败，您不能操作其他实验室的设备")
            return False
        else:
            obj.save()

    def delete_model(self, request, obj):
        if obj.lab_id not in request.user.belong_lab.all() and not request.user.is_superuser:
            messages.error(request, "操作失败，您不能操作其他实验室的设备")
            return False
        else:
            obj.delete()


    def set_is_lend(self, request, queryset):

        if queryset[0].lab_id not in request.user.belong_lab.all() and not request.user.is_superuser:
            messages.error(request, "操作失败，您不能操作其他实验室的设备")
        else:
            for ins in queryset:
                ins.is_lend = True
                ins.save()
            self.message_user(request, "已全部设置为借出")

    def set_not_lend(self, request, queryset):
        if queryset[0].lab_id not in request.user.belong_lab.all() and not request.user.is_superuser:
            messages.error(request, "操作失败，您不能操作其他实验室的设备")
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


class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password',"belong_lab")}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    pass




admin.site.register(Apply, ApplyAdmin)
admin.site.register(Instrument, InstrumentAdmin)
admin.site.register(Lab, LabAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(ApplyInstrumentList)


admin.site.register(MyUser,MyUserAdmin)

admin.site.site_title = u"哈医大实验室服务平台后台管理"
admin.site.site_header = u"哈医大实验室服务平台后台管理"