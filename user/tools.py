import requests
from django.http import HttpResponse
import json

def CrossDomainReturn(result):
    response = HttpResponse(json.dump(result), content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response['Access-Control-Max-Age'] = '1000'
    response['Access-Control-Allow-Headers'] = '*'
    return response