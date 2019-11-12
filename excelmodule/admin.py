from django.contrib import admin
from .models import ExcelImporter
from user.models import Instrument
import xlrd
# Register your models here.


# @admin.register(testClass)
class ExcelImporterAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save()
        print(obj.excel_file.path)
        st = xlrd.open_workbook(obj.excel_file.path).sheets()[0]

        attr_info = {
            # 每一项带有该项的excel中的对应名称（key)，model对应属性(attr_name)
            # 对应excel列数 (matchColumnNum)该项需要根据列名学习，默认-1
            "仪器编号":{"attr_name": "model_number", "matchColumnNum": -1},
            "仪器名称":{"attr_name": "name", "matchColumnNum": -1},
            "型号":{"attr_name": "model_type", "matchColumnNum": -1},
            "厂家":{"attr_name": "maker", "matchColumnNum": -1},
            "类别":{"attr_name": "type", "matchColumnNum": -1},
            "数量":{"attr_name": "number", "matchColumnNum": -1},
        }

        # # default = ["暂无", "暂无", "暂无", "暂无", "暂无", 1]
        # attr_name = ["model_number", "name", "number", "maker", "type"]
        # order = [-1, -1, -1, -1, -1, -1]
        # 建立由仪器类型到列的映射
        for columnNum, item in enumerate(st.row(0)):
            if item.value in attr_info.keys():
                attr_info[item.value]["matchColumnNum"] = columnNum

        for i in range(1, st.nrows):
            # todo:获取数量
            num = 1
            order = attr_info["数量"]["matchColumnNum"]
            # 判断该列存在且值为数字 2代表值为num
            if order != -1 and st.cell(i, order).ctype == 2:
                num = st.cell_value(i, order)
            for k in range(int(num)):
                ins = Instrument()
                for j in attr_info.keys():
                    if j == "数量": continue
                    idx = attr_info[j]["matchColumnNum"]
                    attr_name = attr_info[j]["attr_name"]
                    # 值存在且为文本
                    if st.cell(i, idx).ctype == 1:
                        setattr(ins, attr_name, st.cell_value(i, idx))
                    # 否则不设置，则为默认值
                ins.lab_id = obj.lab_id
                ins.is_lend = False
                ins.save()






admin.site.register(ExcelImporter, ExcelImporterAdmin)