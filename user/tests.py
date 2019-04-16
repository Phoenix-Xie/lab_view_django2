from django.test import TestCase, Client
from django.urls import reverse
import json
# Create your tests here.
from .views import lab_long, instrument_long, department_long


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

