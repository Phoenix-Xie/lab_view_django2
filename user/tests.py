from django.test import TestCase, Client
from django.urls import reverse
import json
# Create your tests here.

class LabListViewTests(TestCase):
    def test_not_number_args(self):
        client = Client()
        url = reverse('user:Home')
        response = client.get(url)
        a = json.loads(response.content)
        self.assertEqual('Hello world', a['hello'])