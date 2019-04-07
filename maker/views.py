from django.http import HttpResponse

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

import json
import sqlite3
# import sql_operation

from .sql_operation import *
from .complicated_sql import get_efficient_currency, get_burst_currency


def index(request):

    # load or get data
    # d = load_data()
    d = get_data_from_cache()
    update_news('init', 'hihi', 'http://images.firstcovers.com/covers/flash/f/final_exams-1558705.jpg?i', \
            'Hello World!', 'Trump')

    # schedule the timeslot
    update_timeslot()
    makeup_timeslot()

    # insert enough currency infomation
    for i in range(108):
        update_currency('make', id=d[i]['id'])

    # test the delete of currency
    delete_currency(name='Bitcoin')

    # test the select of currency

    tmp = d[2]['name']
    if not delete_currency(id=1):
        print('2nd delete failed. Test passed.')

    return HttpResponse("Hello, world. You're at the maker index. Bitcoin is: %s" % tmp)



def adv1(request, price1, price2):
    # t1: March 28, 2019 6:00:00 PM
    # t2: March 28, 2019 5:00:00 PM
    # t3: March 28, 2019 12:00:00 AM
    res = get_burst_currency(431615, 431614, 431621, price1, price2)
    res_json = json.dumps(res)
    return HttpResponse(res_json)

def adv2(request, price):
    res = get_efficient_currency(price)
    res_json = json.dumps(res)
    return HttpResponse(res_json)
