# coding: UTF-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import View
# Create your views here.
from django.views import View

from user.tools import getOpenId
from .models import Lab, Instrument, Apply, ApplyInstrumentList, Department
from django.core.paginator import Paginator, EmptyPage
import datetime
# 状态码声明
'''
状态码列表
1 成功
0 内容为空
-1 无效请求
-2 字符串过长
-3 参数不正确
-4 所查询id不存在
'''
# 部署条件注意
'''
1. 注意将本文件中所有print语句注释，防止由于服务器python为ascii无法打印中文导致报错
'''
# 字符串长度设置
lab_long = 20
instrument_long = 50
department_long = 20
lab_page_num = 5
insturment_page_num = 5
department_page_num = 5
add_data = False


class Tools:
    @staticmethod
    def get_head_id_and_number(request):
        try:
            head_id = int(request.GET["head_id"])
            number = int(request.GET["number"])
            return head_id, number
        except ValueError as e:
            raise e
        except Exception:
            raise Exception

    @staticmethod
    def bad_request():
        data = {
            'statu': -1,
            'msg': "异常请求",
        }
        return data

    @staticmethod
    def bad_request_content():
        data = {
            'statu': -1,
            'msg': "请求内容文本有误，请详细检查是否按要求提供接口所需内容数据",
        }
        return data

    @staticmethod
    def too_long():
        data = {
            'statu': -2,
            'msg': "字符串过长",
        }
        return data

    @staticmethod
    def head_id_and_number_error():
        data = {
            "statu": -3,
            "msg": "head_id或number非数字"
        }
        return data

    @staticmethod
    def id_is_not_exist():
        data = {
            "statu": -4,
            "msg": "id不存在"
        }
        return data

    @staticmethod
    def id_is_not_a_number():
        data = {
            "statu": -3,
            "msg": "id不是数字"
        }
        return data

    @staticmethod
    def page_is_not_a_number():
        data = {
            "statu": -3,
            "msg": "page不是数字"
        }
        return data

    @staticmethod
    def page_number_is_not_a_number():
        data = {
            "statu": -3,
            "msg": "page或number不是数字"
        }
        return data

    @staticmethod
    def page_empty():
        data = {
            'statu': 0,
            'msg': '该页内容为空',
        }
        return data

    @staticmethod
    def return_department_list(obj_list, page=1):
        p = Paginator(obj_list, department_page_num)
        try:
            obj_list = p.page(page).object_list
        except Exception as e:
            raise e
        obj_info = []
        for obj in obj_list:
            obj_info.append(
                {
                    'id': obj.id,
                    'name': obj.name,
                }
            )
        return obj_info

    @staticmethod
    def return_lab_list(obj_list, page=1):
        p = Paginator(obj_list, lab_page_num)
        try:
            obj_list = p.page(page).object_list
        except Exception as e:
            raise e
        obj_info = []
        for obj in obj_list:
            obj_info.append(
                {
                    'id': obj.id,
                    'name': obj.name,
                    'department_id': obj.department_id.id,
                    'department_name': obj.department_id.name,
                }
            )
        return obj_info

    @staticmethod
    def return_instrument_list(obj_list, page=1):
        p = Paginator(obj_list, insturment_page_num)
        try:
            obj_list = p.page(page).object_list
        except Exception as e:
            raise e
        obj_info = []
        for obj in obj_list:
            obj_info.append(
                {
                    'id': obj.id,
                    'number': obj.number,
                    'name': obj.name,
                    'model_number': obj.model_number,
                    'maker': obj.maker,
                    'type': obj.type,
                    'lab_id': obj.lab_id.id,
                    'lab_name': obj.lab_id.name,
                    'is_lend': obj.is_lend,
                }
            )

        return obj_info


class Home(View):

    """
    主页
    """
    def get(self, request):
        data = {
            "hello": "Hello world"
        }
        return JsonResponse(data)


# 分页接口
class Page(View):
    def __init__(self):
        super().__init__()
        self.obj_model = Instrument.objects

    def return_func(self, obj_list, page):
        return Tools.return_instrument_list(obj_list, page)

    def get(self, request):
        try:
            page = int(request.GET['page'])
            # number = int(request.GET['number'])
        except ValueError:
            return JsonResponse(Tools.id_is_not_a_number())
        except Exception:
            return JsonResponse(Tools.bad_request())

        # print(page)
        obj_list = self.obj_model.all().order_by('id')
        try:
            obj_list = self.return_func(obj_list, page)
            # print(obj_list)
        except EmptyPage:
            data = {
                'statu': 0,
                'msg': '该页内容为空',
            }
            return JsonResponse(data)
        except Exception:
            return JsonResponse(Tools.bad_request())


        data = {
            'statu': 1,
            'msg': '获取成功',
            'result': obj_list
        }
        # print(data)
        return JsonResponse(data, status=200)


class DepartmentPage(Page):
    def __init__(self):
        super().__init__()
        self.obj_model = Department.objects

    def return_func(self, obj_list, page):
        return Tools.return_department_list(obj_list, page)


class LabPage(Page):
    def __init__(self):
        super().__init__()
        self.obj_model = Lab.objects

    def return_func(self, obj_list, page):
        return Tools.return_lab_list(obj_list, page)


class InstrumentPage(Page):
    def __init__(self):
        super().__init__()
        self.obj_model = Instrument.objects

    def return_func(self, obj_list, page):
        return Tools.return_instrument_list(obj_list, page)


# 列表接口
class List(View):
    def return_func(self, obj_list):
        return Tools.return_department_list(obj_list)

    def def_model(self):
        self.model_obj = Department.objects

    def get(self, request):
        self.def_model()
        try:
            head_id, number = Tools.get_head_id_and_number(request)
        except ValueError:
            return JsonResponse(Tools.head_id_and_number_error(), status=200)
        except Exception:
            return self.other(request)

        obj_list = self.model_obj \
            .all() \
            .order_by('id') \
            .filter(id__gte=head_id) \
            .filter(id__lte=(head_id + number))

        data = {
            'statu': 1,
            'msg': '获取成功',
            'number': len(obj_list),
            'result': self.return_func(obj_list)
        }
        # print(data)
        return JsonResponse(data, status=200)

    def other(self, request):
        data = {
            'statu': -1,
            'msg': '异常请求',
        }
        # print(data)
        return JsonResponse(data, status=500)


class DepartmentList(List):
    def return_func(self, obj_list):
        return Tools.return_department_list(obj_list)

    def def_model(self):
        self.model_obj = Department.objects


class LabList(List):
    def return_func(self, obj_list):
        return Tools.return_lab_list(obj_list)

    def def_model(self):
        self.model_obj = Lab.objects


class InstrumentList(List):
    def return_func(self, obj_list):
        return Tools.return_instrument_list(obj_list)

    def def_model(self):
        self.model_obj = Instrument.objects


# 根据名称寻找
class FindWithName(View):
    """
    需要制定limit函数和return_func函数
    """
    def __init__(self):
        super().__init__()
        self.long = lab_long
        self.obj_model = Lab.objects

    def return_func(self, obj_list, page=1):
        return Tools.return_lab_list(obj_list, page)

    def get(self, request):
        try:
            name = request.GET['name']
            page = int(request.GET.get('page', 1))
        except ValueError:
            return JsonResponse(Tools.page_is_not_a_number())
        except Exception:
           return self.other(request)

        if len(name) > self.long:
            return JsonResponse(Tools.too_long(), status=400)
        try:
            obj_list = self.obj_model.filter(name__contains=name).order_by('id')
        except Exception:
            data = {
                'statu': 0,
                'msg': '查无此信息',
            }
            # print(data)
            return JsonResponse(data, status=200)

        # print(name)
        # print(page)
        try:
            obj_list = self.return_func(obj_list, page)
            # print('test')
        except EmptyPage:
            return JsonResponse(Tools.page_empty())
        except Exception:
            return JsonResponse(Tools.bad_request())

        data = {
            'statu': 1,
            'msg': '获取成功',
            'result': obj_list
        }
        return JsonResponse(data, status=200)

    def other(self, request):
        data = {
            'statu': -1,
            'msg': '无效请求',
        }
        return JsonResponse(data, status=200)


class FindDepartmentWithName(FindWithName):
    def __init__(self):
        super().__init__()
        self.long = department_long
        self.obj_model = Department.objects

    def return_func(self, obj_list, page=1):
        return Tools.return_department_list(obj_list, page)


class FindLabWithName(FindWithName):
    """
    找到指定名字的实验室
    """

    def __init__(self):
        super().__init__()
        self.long = lab_long
        self.obj_model = Lab.objects

    def return_func(self, obj_list, page=1):
        return Tools.return_lab_list(obj_list, page)


class FindInstrumentWithName(FindWithName):
    def __init__(self):
        super().__init__()
        self.long = instrument_long
        self.obj_model = Instrument.objects

    def return_func(self, obj_list, page=1):
        return Tools.return_instrument_list(obj_list, page)


# 根据id寻找
class FindWithId(View):
    """
    根据id获取仪器
    """
    def __init__(self):
        super().__init__()
        self.obj_model = Instrument.objects

    def return_func(self, obj_list):
        return Tools.return_instrument_list(obj_list)

    def get(self, request):

        try:
            id = int(request.GET['id'])
        except ValueError:
            return JsonResponse(Tools.id_is_not_a_number())
        except Exception:
            return JsonResponse(Tools.bad_request())

        try:
            obj = self.obj_model.get(id=id)
        except Exception:
            return JsonResponse(Tools.id_is_not_exist())

        data = {
            'statu': 1,
            'msg': '获取成功',
            'result': self.return_func([obj])
        }
        return JsonResponse(data, status=200)


class FindInstrumentWithId(FindWithId):
    """
    根据id获取仪器
    """
    def __init__(self):
        super().__init__()
        self.obj_model = Instrument.objects

    def return_func(self, obj_list):
        return Tools.return_instrument_list(obj_list)


class FindLabWithId(FindWithId):
    """
    根据id获取仪器
    """
    def __init__(self):
        super().__init__()
        self.obj_model = Lab.objects

    def return_func(self, obj_list):
        return Tools.return_lab_list(obj_list)


class FindDepartmentWithId(FindWithId):
    def __init__(self):
        super().__init__()
        self.obj_model = Department.objects

    def return_func(self, obj_list):
        return Tools.return_department_list(obj_list)


# 申请
class ApplyInstrument(View):
    """
    申请仪器
    """
    def post(self, request):
        try:
            email = request.POST.get('email')
            name = request.POST.get('name')
            text = request.POST.get('text')
            instrument_list = request.POST.get('instrument_id')
            openId = request.POST.get("openId", None)
            formId = request.POST.get("formId", None)
        except Exception as e:
            return JsonResponse(Tools.bad_request())
        if email == None:
            data = {
                "statu": -1,
                "msg": "请填入邮件，检查是否正确使用接口",
            }
            return JsonResponse(data)
        if name == None:
            data = {
                "statu": -1,
                "msg": "请填入姓名，检查是否正确使用接口",
            }
            return JsonResponse(data)
        if text == None:
            data = {
                "statu": -1,
                "msg": "请填入文本，检查是否正确使用接口",
            }
            return JsonResponse(data)
        if instrument_list == None:
            data = {
                "statu": -1,
                "msg": "请填入仪器id列表，检查是否正确使用接口",
            }
            return JsonResponse(data)
        if openId == None:
            data = {
                "statu": -1,
                "msg": "请填入openId，检查是否正确使用接口",
            }
            return JsonResponse(data)
        if formId == None:
            data = {
                "statu": -1,
                "msg": "请填入formId，检查是否正确使用接口",
            }
            return JsonResponse(data)

        time = datetime.datetime.now()
        for id in instrument_list.split(' '):
            instrument = Instrument.objects.filter(id=id, is_lend=False)
            if instrument.count() == 0:
                data = {
                    "statu": -1,
                    "msg": "部分仪器不存在或已经借出",
                    "not_exit_id": id,
                }
                return JsonResponse(data)

        openid=getOpenId(openId)
        apply = Apply(name=name, text=text, time=time, email= email, openId = openid, formId = formId)
        apply.save()
        for id in instrument_list.split(' '):
            instrument = Instrument.objects.get(id=id)
            print(id)
            applyInstrument = ApplyInstrumentList(Apply_id=apply, Instrument_id=instrument)
            applyInstrument.save()

        data = {
            "statu": 1,
            "msg": "成功提交申请",
        }
        return JsonResponse(data)


# 根据上级id查询下级
class FindLabWithDepartmentId(View):
    def get(self, request):
        try:
            id = int(request.GET['id'])
        except ValueError:
            return JsonResponse(Tools.id_is_not_a_number())
        except Exception:
            return JsonResponse(Tools.bad_request())

        try:
            page = int(request.GET.get('page', 1))
        except ValueError:
            return JsonResponse(Tools.page_is_not_a_number())
        except Exception:
            return JsonResponse(Tools.bad_request())

        # 检查department存在
        try:
            d = Department.objects.get(id=id)
        except Exception:
            return JsonResponse(Tools.id_is_not_exist())

        lab_list = Lab.objects.filter(department_id=d).order_by('id')

        try:
            lab_list = Tools.return_lab_list(lab_list, page)
        except EmptyPage:
            return JsonResponse(Tools.page_empty())
        except Exception:
            return JsonResponse(Tools.bad_request())

        data = {
            'statu': 1,
            'msg': '获取成功',
            'number': len(lab_list),
            "result": lab_list
        }
        return JsonResponse(data)


class FindInstrumentWithLabId(View):
    def get(self, request):
        try:
            id = int(request.GET['id'])
        except ValueError:
            return JsonResponse(Tools.id_is_not_a_number())
        except Exception:
            return JsonResponse(Tools.bad_request())

        try:
            page = int(request.GET.get('page', 1))
        except ValueError:
            return JsonResponse(Tools.page_is_not_a_number())
        except Exception:
            return JsonResponse(Tools.bad_request())

        # 检查department存在
        try:
            d = Lab.objects.get(id=id)
        except Exception:
            return JsonResponse(Tools.id_is_not_exist())

        obj_list = Instrument.objects.filter(lab_id=d).order_by('id')

        try:
            obj_list = Tools.return_instrument_list(obj_list, page)
        except EmptyPage:
            return JsonResponse(Tools.page_empty())
        except Exception:
            return JsonResponse(Tools.bad_request())

        data = {
            'statu': 1,
            'msg': '获取成功',
            'number': len(obj_list),
            "result": obj_list
        }
        return JsonResponse(data)


class AddData(View):
    def get(self, request):
        if add_data:
            data = {
                "信息学院": {
                    "计算机视觉": {
                        # number model_number, maker, type, is_lend
                        "计算机": ["001", "001", "海大制造厂", "计算设备", False],
                        "GPU": ["002", "002", "海大制造厂", "计算设备", False]
                    },
                    "计算机算法": {
                        "计算机": ["003", "003", "海大制造厂", "计算设备", False],
                        "计算器": ["004", "004", "海大制造厂", "计算设备", False]
                    }
                },
                "工程学院": {
                    "测绘": {
                        "尺子": ["005", "005", "海大制造厂", "测量设备", False],
                        "测绘仪": ["006", "006", "海大制造厂", "测量设备", False]
                    },
                    "机床": {
                        "机车": ["007", "007", "海大制造厂", "加工设备", False],
                        "车床": ["008", "008", "海大制造厂", "加工设备", False]
                    }
                },
                '文新学院': {

                },
                '外国语学院': {

                }
            }

            for i in data.items():
                d = Department(name=i[0])
                d.save()
                for j in data[i[0]].items():
                    l = Lab(name=j[0], department_id=d)
                    l.save()
                    for k in data[i[0]][j[0]].items():
                        ins = Instrument(
                            name=k[0],
                            number=k[1][0],
                            model_number=k[1][1],
                            maker=k[1][2],
                            type=k[1][3],
                            is_lend=k[1][4],
                            lab_id=l,
                        )
                        # print("-", ins.name)
                        ins.save()
        return HttpResponse("成功添加")