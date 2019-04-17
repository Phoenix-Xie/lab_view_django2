from django.test import TestCase, Client
from django.urls import reverse
import json
# Create your tests here.
from .views import lab_long, instrument_long, department_long
from .models import Department, Lab, Instrument
add_data = True


#  列表接口测试
class DepartmentListViewTests(TestCase):
    def test_can_work(self):
        client = Client()
        url = reverse('user:DepartmentList')+"?head_id=0&number=2"
        response = client.get(url)
        self.assertEqual(200, response.status_code)


class LabListViewTests(TestCase):
    def test_can_work(self):
        client = Client()
        url = reverse('user:LabList')+"?head_id=0&number=2"
        response = client.get(url)
        self.assertEqual(200, response.status_code)


class InstrumentListViewTests(TestCase):
    def test_can_work(self):
        client = Client()
        url = reverse('user:InstrumentList')+"?head_id=0&number=2"
        response = client.get(url)
        self.assertEqual(200, response.status_code)


# 根据名称寻找
class FindLabWithNameViewTest(TestCase):
    def test_can_work(self):
        client = Client()
        url = reverse('user:FindLabWithName')+"?name="
        response = client.get(url)
        self.assertEqual(200, response.status_code)

    def test_too_long_name(self):
        a = ''
        for i in range(lab_long+1):
            a = a + '1'
        url = reverse('user:FindLabWithName') + "?name=" + a
        client = Client()
        response = client.get(url)
        a = json.loads(response.content)
        self.assertEqual(-2, a['statu'])


class FindInstrumentWithNameViewTest(TestCase):
    def test_can_work(self):
        client = Client()
        url = reverse('user:FindInstrumentWithName') + "?name="
        response = client.get(url)
        self.assertEqual(200, response.status_code)

    def test_too_long_name(self):
        a = ''
        for i in range(instrument_long+1):
            a = a + '1'
        url = reverse('user:FindInstrumentWithName') + "?name=" + a
        client = Client()
        response = client.get(url)
        a = json.loads(response.content)
        self.assertEqual(-2, a['statu'])


class FindDepartmentWithNameViewTest(TestCase):
    def test_can_work(self):
        client = Client()
        url = reverse('user:FindDepartmentWithName') + "?name="
        response = client.get(url)
        self.assertEqual(200, response.status_code)

    def test_too_long_name(self):
        a = ''
        for i in range(department_long+1):
            a = a + '1'
        url = reverse('user:FindDepartmentWithName') + "?name=" + a
        client = Client()
        response = client.get(url)
        a = json.loads(response.content)
        self.assertEqual(-2, a['statu'])


# 根据id寻找
class FindInstrumentWithIdViewTest(TestCase):
    def test_can_work(self):
        client = Client()
        url = reverse('user:FindInstrumentWithId') + "?id=0"
        response = client.get(url)
        self.assertEqual(200, response.status_code)


class FindLabWithIdViewTest(TestCase):
    def test_can_work(self):
        client = Client()
        url = reverse('user:FindLabWithId') + "?id=0"
        response = client.get(url)
        self.assertEqual(200, response.status_code)


class FindDepartmentWithIdViewTest(TestCase):
    def test_can_work(self):
        client = Client()
        url = reverse('user:FindDepartmentWithId') + "?id=0"
        response = client.get(url)
        self.assertEqual(200, response.status_code)


class ApplyInstrumentViewTest(TestCase):
    pass


class FindLabWithDepartmentIdViewTest(TestCase):
    def test_can_work(self):
        client = Client()
        url = reverse('user:FindLabWithDepartmentId') + "?id=0"
        response = client.get(url)
        self.assertEqual(200, response.status_code)


class FindInstrumentWithLabIdViewTest(TestCase):
    def test_can_work(self):
        client = Client()
        url = reverse('user:FindInstrumentWithLabId') + "?id=0"
        response = client.get(url)
        self.assertEqual(200, response.status_code)


# 数据添加
class addData(TestCase):
    def test_add_data(self):
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
                        print("-", ins.name)
                        ins.save()

