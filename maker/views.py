from django.http import HttpResponse

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

import json
import sqlite3
# import sql_operation

from .sql_operation import *
from .complicated_sql import *

# dependent of advance function 1
import numpy
import collections
import operator


def index(request):
    mode = ['load', 'get', 'no', 'yes']     # [load/get data, get/make timeslot, delete?, load news?]
    print('\nMode here: ')
    print('Load/get data: ', mode[0])
    print('Get/make timeslot: ', mode[1])
    print('Test delete? ', mode[2])
    print('Load news?', mode[3], '\n')

    # load or get data
    print('Obtaining data...')
    if mode[0] == 'load':
        d = load_data()
    else:
        d = get_data_from_cache()
    

    # get news
    # update_news('init', 'hihi', 'http://images.firstcovers.com/covers/flash/f/final_exams-1558705.jpg?i', 'Hello World!', 'Trump')
    
    if mode[3] == 'yes':
        print('Loading news...')
        load_news()

    # schedule the timeslot
    print('Updating timeslot...')
    if mode[1] == 'get':
        update_timeslot()
    else:
        makeup_timeslot()
    
    # complete timeslot
    print('Completing timeslot...')
    complete_time()

    # insert enough currency infomation
    print('Updating currency...')
    for i in range(108):
        if mode[1] == 'get':
            update_currency('get', id=d[i]['id'])
        else:
            update_currency('make', id=d[i]['id'])

    # test the delete of currency
    if mode[2] == 'yes':
        delete_currency(name='Bitcoin')
        print('Delete Bitcoin!')
    else:
        print('Delete not tested.')

    # test the select of currency
    tmp = d[1]['name']
    print()

    return HttpResponse("Hello, world. You're at the maker index. The coin is: %s" % tmp)

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

def get_currency(request, name):
     
    # # name = request.kwargs['name']
    # name = request.query_params.get('name', None)
    print('\n\nname = ', name, '\n\n')

    with connection.cursor() as cursor:
        cursor.execute('''SELECT * FROM maker_cryptocurrency c, maker_metric m 
            WHERE c.id = m.crypto_currency_id AND c.name LIKE '%%%s%%' AND m.timeslot_id = (
            SELECT MAX(timeslot_id) FROM maker_metric WHERE crypto_currency_id = c.id 
        )''' % name)
        res = dictfetchall(cursor)
    res_json = json.dumps(res)
    return HttpResponse(res_json)

# Get currency with highest utility, see comment of get_best_coin_by_name()
def get_best_currency(request, name):
    print('\n\nname = ', name, '\n\n')
    
    res = get_best_coin_by_name(name)
    res_json = json.dumps(res)
    return HttpResponse(res_json)

# Get news that includes given word, see comment of get_news_by_word()
def get_news(request, word):
    print('\n\nword = ', word, '\n\n')
    res = get_news_by_word(word)
    res_json = json.dumps(res)
    return HttpResponse(res_json)

def all_history(request):
    print('\n\ninserting all history...')
    insert_all_history()
    return HttpResponse('All history inserted!')

    # print('\n\npatch: repairing volume...')
    # insert_all_volume()
    # return HttpResponse('All volume repaired...')

def all_coin(request):
    print('\n\nupdating all coins...')
    insert_all_coin()
    return HttpResponse('All coins inserted!')