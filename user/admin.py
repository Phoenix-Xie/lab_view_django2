from django.contrib import admin
# xie  123456
# Register your models here.
from .models import Instrument, Lab, Department, ApplyInstrumentList, Apply


admin.site.register(Instrument)
admin.site.register(Lab)
admin.site.register(Department)
admin.site.register(ApplyInstrumentList)


class ApplyInstrumentListInline(admin.StackedInline):
    model = ApplyInstrumentList
    extra = 3


class ApplyAdmin(admin.ModelAdmin):
    inlines = [ApplyInstrumentListInline]


admin.site.register(Apply, ApplyAdmin)