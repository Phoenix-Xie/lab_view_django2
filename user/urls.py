"""lab_view_django2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
app_name = 'user'
urlpatterns = [
    path('test', views.Home.as_view(), name='Home'),
    path('FindLabWithName', views.FindLabWithName.as_view(), name='FindLabWithName'),
    path('LabList', views.LabList.as_view(), name='LabList'),
    path('InstrumentList', views.InstrumentList.as_view(), name='InstrumentList'),
    path('FindInstrumentWithId', views.FindInstrumentWithId.as_view(), name='FindInstrumentWithId'),
    path('FindInstrumentWithName', views.FindInstrumentWithName.as_view(), name='FindInstrumentWithName'),
    path('ApplyInstrument', views.ApplyInstrument.as_view(), name='ApplyInstrument'),
    path('DepartmentList', views.DepartmentList.as_view(), name='DepartmentList'),
    path('FindDepartmentWithName', views.FindDepartmentWithName.as_view(), name='FindDepartmentWithName'),
    path('FindLabWithDepartmentId', views.FindLabWithDepartmentId.as_view(), name='FindLabWithDepartmentId'),
    path('FindInstrumentWithLabId', views.FindInstrumentWithLabId.as_view(), name='FindInstrumentWithLabId'),
    path('FindLabWithId', views.FindLabWithId.as_view(), name='FindLabWithId'),
    path('FindDepartmentWithId', views.FindDepartmentWithId.as_view(), name='FindDepartmentWithId'),
    # 分页
    path('DepartmentPage', views.DepartmentPage.as_view(), name='DepartmentPage'),
    path('LabPage', views.LabPage.as_view(), name='LabPage'),
    path('InstrumentPage', views.InstrumentPage.as_view(), name='InstrumentPage'),
    # 添加数据
    path('AddData', views.AddData.as_view(), name='AddData')
]
