# coding: UTF-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import View
# Create your views here.
from django.views import View
from django.views.generic import ListView
from . import models
from .models import Lab, Instrument, Apply, ApplyInstrumentList
import chardet
import datetime


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
        print(name)

        # print(chardet.detect("有毒".encode()))
        # print(chardet.detect(name.encode().decode("UTF-8").encode()))
        # name = name.encode("iso-8859-1").decode('utf8')
        print(name)
        lab_list = Lab.objects.filter(name__contains=name)
        # print(lab_list)
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
        headId = request.GET["headId"]
        number = request.GET["number"]
        lab_list = Lab.objects.all().order_by("id")[headId: headId+number]
        lab_info = []
        for lab in lab_list:
            lab_info.append(
                {
                    'id': lab.id,
                    'name': lab.name,
                    'department_id': lab.department_id,
                }
            )
        data = {
            'statu': 1,
            'msg': '获取成功',
            "labs": lab_info,
        }
        return HttpResponse(data)


class InstrumentList(View):
    """
    仪器列表
    """
    def get(self, request):
        lab_id = request.GET['lab_id']
        instrument_list = Instrument.objects.filter(lab_id=lab_id)

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
                    'lab_id':instrument.lab_id,
                    'is_lend': instrument.is_lend,
                }
            )

        data={
            'statu': 1,
            'msg': '获取成功',
            'result': instrument_list
        }
        return JsonResponse(data, status=200)


class FindInstrumentWithId(View):
    """
    根据id获取仪器
    """
    def get(self, request):
        id = request.GET['id']
        instrument_list = Instrument.objects.get(id=id)
        if instrument_list == None:
            data = {
                'statu': -2,
                'msg': '不存在该仪器',
            }
            return JsonResponse(data)
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
                    'lab_id': instrument.lab_id,
                    'is_lend': instrument.is_lend,
                }
            )

        data = {
            'statu': 1,
            'msg': '获取成功',
            'result': instrument_list
        }
        return JsonResponse(data, status=200)


class FindInstrumentWithName(View):
    """
    根据仪器名称获取仪器列表
    """
    def get(self, requst):
        name = requst.GET['name']
        instrument_list = Instrument.objects.filter(name__contains=name)
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
                    'lab_id': instrument.lab_id,
                    'is_lend': instrument.is_lend,
                }
            )

        data = {
            'statu': 1,
            'msg': '获取成功',
            'result': instrument_list
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

        apply = Apply(title=title, text=text, time=time, email=email)
        apply.save()
        for id in instrument_list:
            applyInstrument = ApplyInstrumentList(Apply_id=apply.id, Instrument_id=id)



