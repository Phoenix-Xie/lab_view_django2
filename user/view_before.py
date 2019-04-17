

# class DepartmentList(View):
#     def get(self, request):
#
#         try:
#             head_id, number = Tools.get_head_id_and_number(request)
#         except ValueError:
#             return JsonResponse(Tools.head_id_and_number_error(), status=200)
#         except Exception:
#             return self.other(request)
#
#         obj_list = Department.objects \
#             .all() \
#             .order_by('id') \
#             .filter(id__gte=head_id) \
#             .filter(id__lte=(head_id + number))
#
#         data = {
#             'statu': 1,
#             'msg': '获取成功',
#             'number': len(obj_list),
#             'result': Tools.return_department_list(obj_list)
#         }
#         # print(data)
#         return JsonResponse(data, status=200)
#
#     def other(self, request):
#         data = {
#             'statu': -1,
#             'msg': '异常请求',
#         }
#         # print(data)
#         return JsonResponse(data, status=500)


# class LabList(View):
#     """
#     实验室列表
#     """
#     def get(self, request):
#
#         try:
#             head_id, number = Tools.get_head_id_and_number(request)
#         except ValueError:
#             return JsonResponse(Tools.head_id_and_number_error(), status=200)
#         except Exception:
#             return self.other(request)
#
#         # 处理逻辑
#         lab_list = Lab.objects.all()\
#             .order_by("id")\
#             .filter(id__gte=head_id)\
#             .filter(id__lte=(number+head_id))
#
#         data = {
#             'statu': 1,
#             'msg': '获取成功',
#             'number': len(lab_list),
#             "labs": Tools.return_lab_list(lab_list),
#         }
#         return JsonResponse(data)
#
#     def other(self, request):
#         data = {
#             'statu': -1,
#             'msg': '无效请求',
#         }
#         return JsonResponse(data, status=500)


# class InstrumentList(View):
#     """
#     仪器列表
#     """
#     def get(self, request):
#
#         try:
#             head_id, number = Tools.get_head_id_and_number(request)
#         except ValueError:
#             return JsonResponse(Tools.head_id_and_number_error(), status=200)
#         except Exception:
#             return self.other(request)
#
#         obj_list = Instrument.objects\
#             .all()\
#             .order_by('id')\
#             .filter(id__gte=head_id)\
#             .filter(id__lte=(head_id+number))
#
#         data = {
#             'statu': 1,
#             'msg': '获取成功',
#             'number': len(obj_list),
#             'result': Tools.return_instrument_list(obj_list)
#         }
#         # print(data)
#         return JsonResponse(data, status=200)

