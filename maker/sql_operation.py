from django.http import HttpResponse
from django.db import connection
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from maker.models import *

import datetime
import json
import sqlite3
import math
import random
#import pymysql

def get_tid():
    return math.floor(timezone.now().timestamp() / 3600)    # now divide by hour, able to change

def update_news(tag, ttype, picture, content, author):
    update_news.i += 1
    with connection.cursor() as cursor:
        cursor.execute("INSERT OR REPLACE INTO maker_relatednews (id, tag, ttype, picture, content, author) \
            VALUES(%s, %s, %s, %s, %s, %s)", [update_news.i, tag, ttype, picture, content, author])
    
update_news.i = 0       # temp use

'''
    Schedule time and load data every time slot.
'''
def update_timeslot():
    tid = get_tid()
    if tid == update_timeslot.id:   # avoid duplicate id
        return
    update_timeslot.id = tid
    time = timezone.now().timestamp()       # field type is TimeField, should be ok
    if update_news.i == 0:
        update_news('holder', 'test', 'http://images.firstcovers.com/covers/flash/f/final_exams-1558705.jpg?i', \
            'Exam is coming!', 'Jason')
        nid = 1
    else:
        nid = random.randint(1, update_news.i)
    with connection.cursor() as cursor:
        cursor.execute("INSERT OR REPLACE INTO maker_timeslot (id, time, related_news_id) \
            VALUES(%s, %s, %s)", [tid, time, nid])

update_timeslot.id = 0      # temp use

'''
def update_user():

def update_favorite():

def update_log():

'''

'''
    Delete a certain kind of currency, e.g. delete_currency(name='Bitcoin').
    Return True if success.
'''
def delete_currency(**kwargs):
    for k in kwargs:
        try:
            if k == 'name':
                q = CryptoCurrency.objects.get(name=kwargs[k])
            elif k == 'id':
                q = CryptoCurrency.objects.get(id=kwargs[k])
        except ObjectDoesNotExist:
            print("Object doesn't exist! ")
            return False
        q.delete()
        return True


'''
    Load the data from the API to a dictionary and also a 
    local cache file. Load every time slot.
'''
def load_data():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '120',
        'convert': 'USD',
        #'sort': 'price',
        #'sort_dir':'desc',
        #'cryptocurrency_type':'coins'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '441cb5ae-6618-4110-8db9-df9cba2b05ec',
    }
    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        
        # write into the cache file
        cache = open('cache.txt', 'w')
        cache.write(response.text)
        cache.close()

        return data['data']
    
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
        return 0

'''
    Get crypto currency data from cache but not website API.
    Return the data part of cache, i.e. a list of all entry dictionaries.
'''
def get_data_from_cache():
    cache = open('cache.txt', 'r')
    data_all = json.loads(cache.read())
    cache.close()
    return data_all['data']


'''
    Insert/update the specified record related to crypto currency. 
    Maybe from online or local cache file.
    Input the search keyword like name='bitcoin' or logo='xxx'.
'''
def update_currency(**kwargs):
    data = get_data_from_cache()
    tid = get_tid()             # note tid should already exist in table! or foreign key constraint will fail

    # insert/update the record by keyword, 1 by default
    for r in data:
        for k in kwargs:
            if r[k] == kwargs[k]:
                mid = (tid % 1e6) * (r['id'] % 1e6)
                supply = r['circulating_supply']
                price = r['quote']['USD']['price']
                volume = r['quote']['USD']['volume_24h']
                privacy = 9.0        # in doubt, where privacy in [0, 10]
                utility = (volume / supply) * math.log10(privacy + 1) / price   # formula by intuition

                # connect to database
                with connection.cursor() as cursor:
                    cursor.execute("INSERT OR REPLACE INTO maker_cryptocurrency (id,name,logo) \
                        VALUES(%s,%s,%s)", [r['id'], r['name'], r['slug']] )

                    # here need time slot to determine the metric id
                    cursor.execute("INSERT OR REPLACE INTO maker_metric (id, volume, privacy, price, supply, utility, crypto_currency_id, timeslot_id) \
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", [mid, volume, privacy, price, supply, utility, r['id'], tid] )

