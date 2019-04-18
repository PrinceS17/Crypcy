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

def make_tid():
    return math.floor(get_tid() - 5 + random.randint(0, 10) )

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def update_news(tag, ttype, picture, content, author):
    update_news.i += 1
    with connection.cursor() as cursor:
        cursor.execute("INSERT OR REPLACE INTO maker_relatednews (id, tag, ttype, picture, content, author) \
            VALUES(%s, %s, %s, %s, %s, %s)", [update_news.i, tag, ttype, picture, content, author])
    
update_news.i = 0       # temp use

'''
    Check and update all the times and newsId in timeslot table.
    Ensure the data integrity in timeslot.
'''
def complete_time():
    with connection.cursor() as cursor:
        cursor.execute(''' SELECT timeslot_id AS id FROM maker_metric
            INTERSECT SELECT id FROM maker_timeslot''')
        res1 = dictfetchall(cursor)
        cursor.execute('SELECT COUNT(*) AS cnt FROM maker_relatednews')
        res2 = dictfetchall(cursor)
    
    if len(res1) == 0: return
    num = res2[0]['cnt']
    print('Incomplete timeslot: ', res1)
    print('# News: ', num)

    for i in range(len(res1)):
        tid = res1[i]['id']
        time = tid * 3600
        nid = random.randint(1, num)
        with connection.cursor() as cursor:
            cursor.execute('INSERT OR REPLACE INTO maker_timeslot (id, time, related_news_id) \
            VALUES(%s, %s, %s)', [tid, time, nid])


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
    Make up time in [now - 5, now + 5].
'''
def makeup_timeslot():
    tid = make_tid()
    makeup_timeslot.id = tid
    time = timezone.now().timestamp() - 10
    if update_news.i == 0:
        update_news('holder', 'test', 'http://images.firstcovers.com/covers/flash/f/final_exams-1558705.jpg?i', \
            'Exam is coming!', 'Jason')
        nid = 1
    else:
        nid = random.randint(1, update_news.i)
    with connection.cursor() as cursor:
        cursor.execute("INSERT OR REPLACE INTO maker_timeslot (id, time, related_news_id) \
            VALUES(%s, %s, %s)", [tid, time, nid])

makeup_timeslot.id = 0


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
def load_data(time=None):
    
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    url2 = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/info'
    parameters = {
        'start': '1',
        'limit': '200',
        'convert': 'USD',
        #'sort': 'price',
        #'sort_dir':'desc',
        #'cryptocurrency_type':'coins'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'fc5c03fd-2394-4df2-8e25-20dd037536a0',
    }
    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        
        sym_list = ''
        for i in range(len(data['data'])):
            symbol = data['data'][i]['symbol']
            sym_list += symbol
            if i != len(data['data']) - 1: sym_list += ','
        
        params = {'symbol': sym_list}
        response2 = session.get(url2, params=params)
        data2 = json.loads(response2.text)
        for i in range(len(data['data'])):
            symbol = data['data'][i]['symbol']
            data['data'][i]['description'] = data2['data'][symbol]['description']
        
        # write into the cache file
        if time is None:
            cache = open('cache.txt', 'w')
        else:
            cache = open('cache_%s.txt' % time, 'w')
        resp = json.dumps(data, indent=4)
        cache.write(resp)
        cache.close()

        return data['data']
    
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
        return 0

'''
    Get crypto currency data from cache but not website API.
    Return the data part of cache, i.e. a list of all entry dictionaries.
'''
def get_data_from_cache(time=None):
    if time is None:
        cache = open('cache.txt', 'r')
    else:
        cache = open('cache_%s.txt' % time, 'r')
    data_all = json.loads(cache.read())
    cache.close()
    return data_all['data']


'''
    Insert/update the specified record related to crypto currency. 
    Maybe from online or local cache file.
    Input the search keyword like name='bitcoin' or logo='xxx'.
'''
def update_currency(mode, **kwargs):
    data = get_data_from_cache()
    if mode == 'get':
        tid = get_tid()             # note tid should already exist in table! or foreign key constraint will fail
    elif mode == 'make':
        if makeup_timeslot.id > 0:
            tid = makeup_timeslot.id
        else:
            tid = make_tid()

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

                logo = 'https://s2.coinmarketcap.com/static/img/coins/32x32/%s.png' % r['id']

                # connect to database
                with connection.cursor() as cursor:
                    cursor.execute("INSERT OR REPLACE INTO maker_cryptocurrency (id,name,symbol,logo,description) \
                        VALUES(%s,%s,%s,%s,%s)", [r['id'], r['name'], r['symbol'], logo, r['description']] )

                    # here need time slot to determine the metric id
                    cursor.execute("INSERT OR REPLACE INTO maker_metric (id, volume, privacy, price, supply, utility, crypto_currency_id, timeslot_id) \
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", [mid, volume, privacy, price, supply, utility, r['id'], tid] )

'''
    Load related news from manually collected file. -- Song
'''
def load_news():
    # customized only for the initial content of news.txt, subject to change!
    tags = ['Bitcoin', 'security', 'talk', 'price', 'monitor']
    ttype = [1 for _ in range(5)]
    picture = ['https://cimg.co/w/articles-attachments/3/5ca/6f3b2a6990.jpg',
                'https://cimg.co/w/articles-attachments/3/5ca/5df40be82d.jpg',
                'https://cimg.co/w/articles-attachments/3/5ca/5c3e760583.jpg',
                'https://cimg.co/w/articles-attachments/3/5ca/1ece276e70.jpg',
                'https://cimg.co/w/articles-attachments/3/5ca/6c89e932ab.jpg']

    with open('news.txt') as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    # print(content[2])       # only for test

    for i in range(5):
        update_news(tags[i], ttype[i], picture[i], content[i], '')

'''
    Update historical data and write to Cache for given coin. 
    From crypto compare here. --Song
'''
def load_history(sym):
    api_key = '9e60336ab74b49376ab8d19a2897ad5a23b9235edb1751ebd60cfdec3769f203'
    url = 'https://min-api.cryptocompare.com/data/histohour?fsym=%s&tsym=USD&limit=1000&api_key=%s' % (sym, api_key)

    session = Session()
    try:
        response = session.get(url)
        data = json.loads(response.text)



        
    
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
        return 0
        