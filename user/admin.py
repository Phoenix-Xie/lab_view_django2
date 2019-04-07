from django.contrib import admin
# xie  123456
# Register your models here.
from .models import Instrument, Lab, Department


admin.site.register(Instrument)
admin.site.register(Lab)
admin.site.register(Department)
