# coding: UTF-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import View
# Create your views here.
from django.views import View
from django.views.generic import ListView
from . import models
from .models import Lab, Instrument, Apply, ApplyInstrumentList, Department
import chardet
import datetime


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


class Home(View):
    """
    主页
    """
    def get(self, request):
        data = {
            "hello": "Hello world"
        }
        return JsonResponse(data)


class FindLabWithName(View):
    """
    找到指定名字的实验室
    """
    def get(self, request):
        name = str(request.GET["name"])
        lab_list = Lab.objects.filter(name__contains=name)
        lab_info = []
        for lab in lab_list:
            lab_info.append(
                {
                    'id': lab.id,
                    'name': lab.name,
                    'department_id': lab.department_id.id,
                }
            )
        data = {
            'statu': 1,
            'msg': '获取成功',
            "result": lab_info,
        }
        return JsonResponse(data, status=200)


class LabList(View):
    """
    实验室列表
    """
    def get(self, request):

        try:
            head_id, number = Tools.get_head_id_and_number(request)
        except ValueError:
            data = {
                "statu": -2,
                "msg": "head_id或number非数字"
            }
            return JsonResponse(data, status=200)
        except Exception:
            return self.other(request)

        # 处理逻辑
        lab_list = Lab.objects.all()\
            .order_by("id")\
            .filter(id__gte=head_id)\
            .filter(id__lte=(number+head_id))
        lab_info = []
        for lab in lab_list:
            lab_info.append(
                {
                    'id': lab.id,
                    'name': lab.name,
                    'department_id': lab.department_id.id,
                }
            )
        data = {
            'statu': 1,
            'msg': '获取成功',
            "labs": lab_info,
        }
        return JsonResponse(data)

    def other(self, request):
        data = {
            'statu': -1,
            'msg': '无效请求',
        }
        return JsonResponse(data, status=500)


class InstrumentList(View):
    """
    仪器列表
    """
    def get(self, request):
        head_id = int(request.GET['head_id'])
        number = int(request.GET['number'])
        instrument_list = Instrument.objects\
            .all()\
            .order_by('id')\
            .filter(id__gte=head_id)\
            .filter(id__lte=(head_id+number))

        instrument_info = []
        for instrument in instrument_list:
            instrument_info.append(
                {
                    'id': instrument.id,
                    'number': instrument.number,
                    'name': instrument.name,
                    'model_number': instrument.model_number,
                    'maker': instrument.maker,
                    'type': instrument.type,
                    'lab_id': instrument.lab_id.id,
                    'is_lend': instrument.is_lend,
                }
            )

        data = {
            'statu': 1,
            'msg': '获取成功',
            'result': instrument_info
        }
        # print(data)
        return JsonResponse(data, status=200)


class FindInstrumentWithId(View):
    """
    根据id获取仪器
    """
    def get(self, request):
        id = request.GET['id']
        instrument = Instrument.objects.get(id=id)
        if instrument == None:
            data = {
                'statu': -2,
                'msg': '不存在该仪器',
            }
            return JsonResponse(data)
        instrument_info = []

        instrument_info.append(
            {
                'id': instrument.id,
                'number': instrument.number,
                'name': instrument.name,
                'model_number': instrument.model_number,
                'maker': instrument.maker,
                'type': instrument.type,
                'lab_id': instrument.lab_id.id,
                'is_lend': instrument.is_lend,
            }
        )

        data = {
            'statu': 1,
            'msg': '获取成功',
            'result': instrument_info
        }
        return JsonResponse(data, status=200)


class FindInstrumentWithName(View):
    """
    根据仪器名称获取仪器列表
    """
    def get(self, requst):
        name = requst.GET['name']
        # print(name)
        instrument_list = Instrument.objects.filter(name__contains=name)
        print(instrument_list)
        instrument_info = []
        for instrument in instrument_list:
            instrument_info.append(
                {
                    'id': instrument.id,
                    'number': instrument.number,
                    'name': instrument.name,
                    'model_number': instrument.model_number,
                    'maker': instrument.maker,
                    'type': instrument.type,
                    'lab_id': instrument.lab_id.id,
                    'is_lend': instrument.is_lend,
                }
            )

        data = {
            'statu': 1,
            'msg': '获取成功',
            'result': instrument_info
        }
        return JsonResponse(data, status=200)


class ApplyInstrument(View):
    """
    申请仪器
    """
    def post(self, requst):
        email = requst.POST['email']
        title = requst.POST['title']
        text = requst.POST['text']
        instrument_list = requst.POST['instrument_id']
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

        apply = Apply(title=title, text=text, time=time, email=email)
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


class DepartmentList(View):
    def get(self, request):
        head_id = int(request.GET['head_id'])
        number = int(request.GET['number'])
        object_list = Department.objects \
            .all() \
            .order_by('id') \
            .filter(id__gte=head_id) \
            .filter(id__lte=(head_id + number))

        instrument_info = []
        for obj in object_list:
            instrument_info.append(
                {
                    'id': obj.id,
                    'name': obj.name,
                }
            )

        data = {
            'statu': 1,
            'msg': '获取成功',
            'result': instrument_info
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


class FindDepartmentWithName(View):
    def get(self, request):
        name = request.GET['name']
        obj = Department.objects.get(name__contains=name)

        if obj is None:
            data = {
                'statu': 0,
                'msg': '查无此学院',
            }
            # print(data)
            return JsonResponse(data, status=200)
        else:
            data = {
                'statu': 1,
                'msg': '获取成功',
                'result': {
                    'id': obj.id,
                    'name': obj.name,
                }
            }
            # print(data)
            return JsonResponse(data, status=200)

    def other(self, request):
        data = {
            'statu': -1,
            'msg': '无效请求',
        }
        return JsonResponse(data, status=200)