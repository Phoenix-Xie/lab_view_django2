from django.test import TestCase, Client
from django.urls import reverse
import json
# Create your tests here.
from .views import lab_long, instrument_long, department_long


class LabListViewTests(TestCase):
    def test_not_number_args(self):
        client = Client()
        url = reverse('user:Home')
        response = client.get(url)
        a = json.loads(response.content)
        self.assertEqual('Hello world', a['hello'])


class FindLabWithNameViewTest(TestCase):
    def test_too_long_name(self):
        a = ''
        for i in range(lab_long+1):
            a = a + '1'
        url = reverse('user:FindLabWithName') + "?name=" + a
        client = Client()
        response = client.get(url)
        a = json.loads(response.content)
        self.assertEqual(-2, a['statu'])

    def test_normal(self):
        a = '谭'
        url = reverse('user:FindLabWithName') + "?name=" + a
        client = Client()
        response = client.get(url)
        a = json.loads(response.content)
        self.assertEqual(1, a['statu'])


class FindInstrumentWithNameViewTest(TestCase):
    def test_too_long_name(self):
        a = ''
        for i in range(instrument_long+1):
            a = a + '1'
        url = reverse('user:FindInstrumentWithName') + "?name=" + a
        client = Client()
        response = client.get(url)
        a = json.loads(response.content)
        self.assertEqual(-2, a['statu'])

    def test_normal(self):
        a = 'G'
        url = reverse('user:FindInstrumentWithName') + "?name=" + a
        client = Client()
        response = client.get(url)
        a = json.loads(response.content)
        self.assertEqual(1, a['statu'])


class FindDepartmentWithNameViewTest(TestCase):
    def test_too_long_name(self):
        a = ''
        for i in range(department_long+1):
            a = a + '1'
        url = reverse('user:FindDepartmentWithName') + "?name=" + a
        client = Client()
        response = client.get(url)
        a = json.loads(response.content)
        self.assertEqual(-2, a['statu'])

    def test_normal(self):
        a = 'G'
        url = reverse('user:FindDepartmentWithName') + "?name=" + a
        client = Client()
        response = client.get(url)
        a = json.loads(response.content)
        self.assertEqual(1, a['statu'])
