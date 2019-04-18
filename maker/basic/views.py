from django.http import HttpResponse
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

import json
import sqlite3

from .SQL_Query import *


def index(request):
    return HttpResponse('Welcome to basic operations!')

# Begin --Zou
# remove 1 line of assignment
def sort_by_vol(request):
    res = sort_by_volume()
    return HttpResponse(json.dumps(res))

def search_by_pref(request,pref):
    res = search_by_prefix(pref)
    return HttpResponse(json.dumps(res))

def sort_by_pri(request):
    res = sort_by_price()
    return HttpResponse(json.dumps(res))

def sort_by_sup(request):
    res = sort_by_supply()
    return HttpResponse(json.dumps(res))

def sort_by_util(request):
    res = sort_by_utility()
    return HttpResponse(json.dumps(res))

def filter(request):
    p1 = request.GET.get('price1', '0')
    p2 = request.GET.get('price2', '10000')
    u1 = request.GET.get('utility1', '-1')
    u2 = request.GET.get('utility2', '10000')
    res = filter_coin(p1, p2, u1, u2)
    return HttpResponse(json.dumps(res))

def detail(request):
    id = request.GET.get('id', '')
    name = request.GET.get('name', '')
    res = get_detail(id, name)
    return HttpResponse(json.dumps(res))

